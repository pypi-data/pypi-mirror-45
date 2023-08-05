

"""
Append Entries request message.
"""
APPEND_ENTRIES = 1

"""
Append Entries response message.
"""
APPEND_RESPONSE = 2

"""
Vote request message.
"""
VOTE_REQUEST = 3

"""
Vote response message.
"""
VOTE_RESPONSE = 4


class Message(object):
    """
    A container for RPC messages between consensus nodes.
    """

    def __init__(self, type, sender, recipient, term, mode, data):
        """
        :param type: Type of the message (APPEND_ENTRIES, APPEND_RESPONSE, VOTE_REQUEST, VOTE_RESPONSE)
        :param sender: Name of the sender
        :param recipient: Name of the recipient
        :param term: Current term of the consensus node
        :param mode: Mode of the consensus node (NODE_MODE_ACTIVE, NODE_MODE_PASSIVE, NODE_MODE_RELUCTANT)
        :param data: Data to be sent
        :type type: int
        :type sender: str
        :type recipient: str
        :type term: int
        :type mode: int
        :type data: dict
        """
        self.type = type
        self.sender = sender
        self.recipient = recipient
        self.term = term
        self.mode = mode
        self.data = data

    @staticmethod
    def build(type, node, state, recipient, data):
        """
        :param type: Type of the message (APPEND_ENTRIES, APPEND_RESPONSE, VOTE_REQUEST, VOTE_RESPONSE)
        :param node: Node building the message
        :param state: State building the message
        :param recipient: Recipient of the message
        :param data: Data to be sent
        :type type: int
        :type node: pyraftlog.node.Node
        :type state: pyraftlog.state.State
        :type recipient: str
        :type data: dict
        :return: A built message
        :rtype: Message
        """
        return Message(type, state.name, recipient, state.current_term, node.mode, data)

    def __str__(self):
        if self.type == APPEND_ENTRIES:
            m_type = "APPEND_ENTRIES"
        elif self.type == APPEND_RESPONSE:
            m_type = "APPEND_RESPONSE"
        elif self.type == VOTE_REQUEST:
            m_type = "VOTE_REQUEST"
        elif self.type == VOTE_RESPONSE:
            m_type = "VOTE_RESPONSE"
        else:
            m_type = "UNKNOWN(%2d)" % self.type

        # Reduce the length of entries
        data = {k: (lambda k, x: x[:1] if k == 'entries' else x)(k, v) for k, v in self.data.items()}

        return "{0}[{1}]({2}:{3}|{4})".format(m_type, self.term, self.sender, self.recipient, data)

    def is_response(self):
        """
        :return: True if the message is a type of response, False otherwise
        :rtype: bool
        """
        return self.type in [VOTE_RESPONSE, APPEND_RESPONSE]
