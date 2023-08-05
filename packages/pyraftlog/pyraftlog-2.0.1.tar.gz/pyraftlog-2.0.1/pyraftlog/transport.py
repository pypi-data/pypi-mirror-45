import logging
import socket
import ssl
import threading

import msgpack

import message


class Transport(object):
    """
    An interface to describe how `pyraftlog.message.Message` should be passed between consensus nodes.

    It uses a publish/subscribe model whereby the sender must publish the message and the recipient
    must be subscribed. There is no requirement that a published message must reach the recipient.
    """

    def __init__(self, logger=None):
        """
        :param logger: Logger to be used by the transport
        :type logger: logging.Logger
        """
        self.logger = logger or logging.getLogger(__name__)

    def connected(self):
        """
        List of connected neighbours.

        :rtype: list[str]
        """
        raise NotImplementedError()

    def is_connected(self, recipient):
        """
        :param recipient: Recipient to check
        :type recipient: str
        :return: True if `recipient` is connected
        :rtype: bool
        """
        raise NotImplementedError()

    def publish(self, node, msg):
        """
        Publish the message `msg` from `node` to the recipient specified in the message and
        return their response (if any).

        :param node: Node sending the message
        :param msg: Message being published
        :type node: pyraftlog.node.Node
        :type msg: pyraftlog.message.Message
        :rtype: pyraftlog.message.Message
        """
        raise NotImplementedError()

    def handle_exception(self, recipient, error):
        """
        Handle an exception that was raised during publishing.

        :param recipient: Recipient of the message being published
        :param error: The error that was raised
        :type recipient: str
        :type error: Error
        :rtype: None
        """
        pass

    def subscribe(self, node):
        """
        Subscribe `node` to of its neighbours.

        :param node: Node to subscribe
        :type: pyraftlog.node.Node
        :rtype: None
        """
        raise NotImplementedError()

    def shutdown(self):
        """
        Shutdown the transport and return itself to the state before any node subscribed.

        :rtype: None
        """
        raise NotImplementedError()


class InMemoryTransport(Transport):
    """
    The In Memory transport is for testing purposes and all nodes should created in the same process.
    """

    nodes = {}  # type: dict
    """ A shared dictionary of subscribed node name -> node. """

    def __init__(self, logger=None):
        super(InMemoryTransport, self).__init__(logger)
        self.node_name = None

    def connected(self):
        return self.nodes.keys()

    def is_connected(self, recipient):
        return recipient in self.nodes

    def publish(self, node, msg):
        # "Send" the message if the recipient is connected and return their response
        if self.is_connected(msg.recipient):
            return self.nodes[msg.recipient].on_message(msg)
        else:
            return None

    def subscribe(self, node):
        self.node_name = node.name
        self.nodes[node.name] = node

    def shutdown(self):
        if self.node_name in self.nodes:
            self.nodes.pop(self.node_name)
        self.node_name = None


class SocketTransport(Transport):
    """
    Socket transport uses TCP socket connections to allow consensus nodes on different hosts to form a consensus
    network.

    Nodes that subscribe open a port to listen and accept new connections. This connection is then kept alive while
    there are no exceptions raised. On first raised exception a conversing subscription is closed. New subscription
    conversations are moved into a separate thread to allow for new connections to be established.

    Nodes that publish will attempt to re-use an open connection to the recipient, however if the connection has been
    closed then it will attempt to reconnect to the recipient.
    """

    def __init__(self, port, keep_idle=1, keep_interval=2, keep_count=2, logger=None):
        """
        :param port: Subscription port
        :param keep_idle: TCP keep alive idle time in seconds
        :param keep_interval: TCP keep alive interval in seconds
        :param keep_count: TCP keep failure count (before assuming connection is broken)
        :param logger: Logger to be used by the transport
        :type port: int
        :type keep_idle: int
        :type keep_interval: int
        :type keep_count: int
        :type logger: logging.Logger
        """
        super(SocketTransport, self).__init__(logger)

        self.sub_sock = None
        self.connections = {}
        self.node = None
        self.port = port
        self.sock_keep_idle_sec = keep_idle
        self.sock_keep_interval_sec = keep_interval
        self.sock_keep_count = keep_count

    def connected(self):
        return self.connections.keys()

    def is_connected(self, recipient):
        return recipient in self.connections

    def shutdown(self):
        if self.sub_sock:
            self.sub_sock.close()

        for sock in self.connections.values():
            sock.close()

        self.sub_sock = None
        self.connections = {}

    def _socket(self, server_hostname=None):
        """
        :param server_hostname: Server hostname
        :type server_hostname: str
        :return: An instance of `socket.socket`
        :rtype: socket.socket
        """
        return socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def _set_socket_options(self, sock):
        """
        Set socket options.

        :param sock: Socket to have its options set
        :type sock: socket.socket
        :rtype: None
        """
        sock.settimeout(None)

        sock.setsockopt(socket.SOL_SOCKET, socket.SO_KEEPALIVE, 1)
        sock.setsockopt(socket.IPPROTO_TCP, socket.TCP_KEEPINTVL, self.sock_keep_interval_sec)
        sock.setsockopt(socket.IPPROTO_TCP, socket.TCP_KEEPCNT, self.sock_keep_count)

        # NOTE: OSX does not have this constant defined, so we have to set it conditionally
        if getattr(socket, 'TCP_KEEPIDLE', None) is not None:
            sock.setsockopt(socket.IPPROTO_TCP, socket.TCP_KEEPIDLE, self.sock_keep_idle_sec)

    def _socket_send(self, sock, msg):
        """
        Send a message to another node. We first send the message length, then the message itself.

        :param sock: Socket to send the data through
        :param msg: Message to be sent
        :type sock: socket.socket
        :type msg: pyraftlog.message.Message
        :return: If the data was successfully sent (no guarantee it was received)
        :rtype: bool
        """
        success = True
        try:
            sock.sendall(msgpack.dumps(msg.__dict__))

        except Exception as e:
            self.logger.error('Failed sending message: (%s) %s', type(e), str(e))
            success = False
            # Disconnect from the socket as probably bad
            if msg.recipient in self.connections:
                self.connections.pop(msg.recipient)
            sock.close()
        finally:
            return success

    def _socket_receive(self, node, sock, neighbour):
        """
        Receive a message from another node. We first expect the message length, then the message itself.

        :param node: Node receiving message
        :param sock: Socket to receive a message
        :type node: pyraftlog.node.Node
        :type sock: socket.socket
        :return: The received message
        :rtype: pyraftlog.message.Message
        """
        unpacker = msgpack.Unpacker(raw=False)
        while node.active:
            buf = sock.recv(1024**2)
            if not buf:
                break
            unpacker.feed(buf)
            try:
                return message.Message(**unpacker.unpack())
            except msgpack.exceptions.OutOfData:
                # Raised when the full message has not yet been received
                self.logger.debug('Extended timeout waiting to receive message [%d]', len(buf))
                self.node.extend_timeout(neighbour)
                continue
            except Exception as e:
                self.logger.error('Failed receiving message (%s): %s', type(e).__name__, str(e))
                # Disconnect from the socket as probably bad
                if neighbour in self.connections:
                    self.connections.pop(neighbour)
                sock.close()
                return None

    def _socket_connect(self, recipient):
        """
        :param recipient: Address to connect
        :type recipient: str
        :return: An connection to the recipient
        :rtype: socket.socket
        """
        if recipient in self.connections:
            return self.connections[recipient]

        host, port = recipient.split(':')
        sock = self._socket(host)
        self._set_socket_options(sock)
        sock.connect((host, int(port)))
        self.node.log(logging.INFO, 'Established connection to %s', recipient)

        self.connections[recipient] = sock

        return sock

    def handle_exception(self, recipient, error):
        # Mark the connection as dead
        if recipient in self.connections:
            self.connections[recipient].close()
        if recipient in self.connections:
            self.connections.pop(recipient)

        super(SocketTransport, self).handle_exception(recipient, error)

    def publish(self, node, msg):
        if not self.node:
            self.node = node

        # Get the connection to the message recipient
        sock = self._socket_connect(msg.recipient)

        # Send the given message
        if self._socket_send(sock, msg):
            # Wait for a response
            return self._socket_receive(node, sock, msg.recipient)
        else:
            return None

    def subscribe(self, node):
        if not self.node:
            self.node = node
        self.sub_sock = None
        try:
            self.sub_sock = self._socket()
            self.sub_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self.sub_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)
            self.sub_sock.bind(('0.0.0.0', int(self.port)))
            self.sub_sock.listen(len(node.neighbours))
            while node.active:
                try:
                    client_sock, address = self.sub_sock.accept()
                    self.connections[str(address)] = client_sock
                    self._set_socket_options(client_sock)
                    self.node.log(logging.INFO, 'Accepted connection with %s:%d', address[0], address[1])

                    # Move the conversation to a daemon thread
                    thread = threading.Thread(target=self._subscribe_converse, args=[node, client_sock, address])
                    thread.daemon = True
                    thread.start()

                except Exception as e:
                    self.node.log(logging.CRITICAL, 'Subscribe Error: %s', str(e))
                    pass
        except ValueError as e:
            self.node.log(logging.CRITICAL, 'Subscribe Value Error: %s', str(e))
            return
        finally:
            self.node.log(logging.DEBUG, 'Unsubscribed')
            if self.sub_sock:
                self.sub_sock.close()

    def _subscribe_converse(self, node, client_sock, address):
        """
        Given a open connection `client_sock` receive messages and send appropriate responses.

        :param client_sock: Client's socket
        :param address: Client's address
        :type client_sock: socket.socket
        :type address: str
        :rtype: None
        """
        neighbour = None
        try:
            while node.active:
                msg = self._socket_receive(node, client_sock, neighbour)
                if not msg:
                    break
                neighbour = msg.sender
                self.connections[neighbour] = client_sock
                response = node.on_message(msg)
                if not response:
                    break

                if not self._socket_send(client_sock, response):
                    break
        except Exception as e:
            self.node.log(logging.CRITICAL, 'Subscribe Converse Error: %s', str(e))
        finally:
            if str(address) in self.connections:
                self.connections.pop(str(address))
            if neighbour and neighbour in self.connections:
                self.connections.pop(neighbour)
            client_sock.close()


class SslSocketTransport(SocketTransport):
    """
    SslSocketTransport behaves exactly like SocketTransport except that is securely transmits all messages.
    """

    CIPHERS = 'EECDH+AESGCM:EDH+AESGCM:AES256+EECDH:AES256+EDH'
    """ Allowed ciphers for communication. """

    def __init__(self, port, key_file, crt_file, ca_crt, ciphers=None,
                 keep_idle=1, keep_interval=2, keep_count=2, logger=None):
        """
        :param port: Subscription port
        :param key_file: Path to TLS key file
        :param crt_file: Path to TLS certificate file
        :param ca_crt: Path to TLS certificate authority certificate file
        :param ciphers: Allowed ciphers for communication (defaults to `SslSocketTransport.CIPHERS`)
        :param keep_idle: TCP keep alive idle time in seconds
        :param keep_interval: TCP keep alive interval in seconds
        :param keep_count: TCP keep failure count (before assuming connection is broken)
        :param logger: Logger to be used by the transport
        :type port: int
        :type key_file: str
        :type crt_file: str
        :type ca_crt: str
        :type ciphers: str
        :type keep_idle: int
        :type keep_interval: int
        :type keep_count: int
        :type logger: logging.Logger
        """
        super(SslSocketTransport, self).__init__(port, keep_idle, keep_interval, keep_count, logger)

        self.ciphers = ciphers or SslSocketTransport.CIPHERS
        self.key_file = key_file
        self.crt_file = crt_file
        self.ca_crt = ca_crt

    def _socket(self, server_hostname=None):
        """
        Return a `socket.socket` that will use the provided TLS certificates and keys.
        If `server_hostname` is provided the SSL context will be for server authentication otherwise it will
        create the context for client authentication.

        :param server_hostname: Server hostname
        :type server_hostname: str
        :return: An instance of `socket.socket`
        :rtype: socket.socket
        """
        sock = super(SslSocketTransport, self)._socket()
        if server_hostname:
            context = ssl.create_default_context(ssl.Purpose.SERVER_AUTH, cafile=self.ca_crt)
        else:
            context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH, cafile=self.ca_crt)

        context.options |= ssl.OP_NO_TLSv1 | ssl.OP_NO_TLSv1_1 | ssl.OP_NO_SSLv2 | ssl.OP_NO_SSLv3
        context.load_cert_chain(self.crt_file, self.key_file)
        context.verify_mode = ssl.CERT_REQUIRED

        if self.ciphers:
            context.set_ciphers(self.ciphers)

        if server_hostname:
            context.check_hostname = True
            sock = context.wrap_socket(sock, server_side=False, server_hostname=server_hostname)
        else:
            sock = context.wrap_socket(sock, server_side=True)

        return sock
