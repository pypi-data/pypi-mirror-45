import logging
import time

import message
from .log import Log
from .statistics import Statistics

CHUNK_SIZE = 1000
""" Maximum number of entries to send in a single append entries RPC. """
MAX_CHUNK_BYTES = 1 * 1024 * 1024  # 1MB
""" Maximum number of bytes the entries can sum in a single append entries RPC. """

STATE_MODE_FOLLOWER = 1
""" [default] Followers listen for append entry requests and monitors for election timeouts. """

STATE_MODE_CANDIDATE = 2
""" Candidates have reached an election timeout and are attempting to be elected. """

STATE_MODE_LEADER = 3
""" Leaders have been elected and listen for add entry requests and send heartbeats/missing entries. """

_stateModeNames = {
    STATE_MODE_FOLLOWER: 'follower',
    STATE_MODE_CANDIDATE: 'candidate',
    STATE_MODE_LEADER: 'leader',
    'follower': STATE_MODE_FOLLOWER,
    'candidate': STATE_MODE_CANDIDATE,
    'leader': STATE_MODE_LEADER,
}


def get_state_mode_name(mode):
    return _stateModeNames.get(mode, 'Unknown mode %s' % str(mode))


class State(object):
    """
    The state of a Consensus Node.
    """

    def __init__(self, mode, name, neighbourhood=None):
        """
        :param mode: State mode
        :param name: State name
        :param neighbourhood: List of node names
        :type mode: int
        :type name: str
        :type neighbourhood: list[str]
        """
        self._name = name
        self._mode = mode
        # Persistent state on all nodes
        # latest term server has seen (increases monotonically)
        self.current_term = 1
        # candidate id that received vote in current term
        self.voted_for = {}
        # log entries; each entry contains command for state machine, and term when entry was received by leader
        self.log = Log()

        # Volatile state on all nodes
        # index of highest log entry known to be committed (increases monotonically)
        self.commit_index = 0
        # index of highest log entry applied to state machine (increases monotonically)
        self.last_applied = 0

        # Added values for log reduction
        self.cluster_applied = dict.fromkeys(neighbourhood or [], 0)
        self.log_reduction = False

        # Volatile state on leaders
        # for each node, index of the index log entry to send to that node
        self.next_index = {}
        # for each node, index of highest log entry known to be replicated on node (increases monotonically)
        self.match_index = {}
        for neighbour in neighbourhood or []:
            self.next_index[neighbour] = self.log.next_index(self.log.index())
            self.match_index[neighbour] = 0

        # Volatile state on candidates
        self.votes = {}

        self.statistics = Statistics()
        self.time_in_state = time.time()

    def __setstate__(self, state):
        self.__init__(STATE_MODE_FOLLOWER, '')
        self.__dict__.update(state)

    def __getstate__(self):
        return {
            "current_term": self.current_term,
            "voted_for": self.voted_for,
            "log": self.log,

            "commit_index": self.commit_index,
            "last_applied": self.last_applied,

            "cluster_applied": self.cluster_applied,
            "log_reduction": self.log_reduction,
        }

    def __str__(self):
        return get_state_mode_name(self.mode)

    @property
    def name(self):
        return self._name

    @property
    def mode(self):
        return self._mode

    @mode.setter
    def mode(self, mode):
        """

        :param mode: New state mode
        :type mode: int
        :rtype: bool
        """
        if self._mode == mode:
            return

        self._mode = mode
        if mode == STATE_MODE_CANDIDATE:
            self.current_term += 1
            self.voted_for = {self.current_term: self.name}
            self.votes[self.name] = True

    def get_current_state(self, index):
        """
        @TODO clarify the name of this method and is function.
        Get the log entry at `index`.

        :param index: Position of the entry to get
        :type index: int
        :return: A dictionary containing the term, index, and value
        :rtype: dict|None
        """
        if index == 0:
            entry = self.log.tail()
        else:
            if self.log.contains(index):
                entry = self.log.get(index)
            else:
                return None

        return {
            'last_term': entry[0],
            'last_index': entry[1],
            'last_value': entry[2]
        }

    def set_current_state(self, data):
        """
        @TODO clarify the name of this method and is function.
        Set the current state.

        :param data: Data to set the current state
        :type data: dict
        :rtype: None
        """
        # -1 as append increments cindex before appending log
        self.log.cindex = data['last_index'] - 1
        self.log.append(data['last_term'], data['last_value'])
        self.commit_index = self.log.index()
        self.last_applied = self.log.index()

    def populate(self, from_state):
        """
        Populate the state with the data stored in `from_state`.

        :param from_state: State to populate from
        :type from_state: pyraftlog.state.State|dict
        :rtype: None
        """
        if isinstance(from_state, State):
            self.__dict__.update(from_state.__getstate__())
        elif isinstance(from_state, dict):
            self.__dict__.update(from_state)

    def increment_term(self, name, neighbour):
        """
        Increment the current term of the state if the neighbour has voted in this term.

        :param name: Name of node
        :param neighbour: Neighbour to consider
        :type name: str
        :type neighbour: str
        :return: True if term was incremented
        :rtype: bool
        """
        if neighbour in self.votes or self.voted_for[self.current_term] != name:
            self.current_term += 1
            self.voted_for = {self.current_term: name}
            self.votes = {name: True}
            return True

        return False

    def missing_entries(self, neighbour):
        """
        Check if `neighbour` is missing entries.

        :param neighbour: Neighbour to consider
        :type neighbour: str
        :return: True if the neighbour is missing entries or if the match index is behind our commit index
        :rtype: bool
        """
        if self.mode != STATE_MODE_LEADER:
            return False

        return self.next_index[neighbour] <= self.log.index() or self.match_index[neighbour] < self.commit_index

    def on_vote_request(self, node, msg):
        """
        This is called when there is a vote request.

        :param node: Node receiving vote request
        :param msg: The vote requested message
        :type node: pyraftlog.node.Node
        :type msg: pyraftlog.message.Message
        :return: Response message
        :rtype: pyraftlog.message.Message
        """
        node.log(logging.INFO, 'Vote request received from %s', msg.sender)

        data = msg.data
        # If the candidate's term is behind ours
        if msg.term < self.current_term:
            return self.vote_response_message(node, data['candidate_id'], False)

        # If we haven't voted this term or we voted for this candidate and
        if self.current_term not in self.voted_for or self.voted_for[self.current_term] == data['candidate_id']:
            # If candidate's log is at least as up-to-date as ours
            if self.log.index() <= data['last_log_index']:
                node.log(logging.INFO, 'Casting vote for %s', msg.sender)
                self.voted_for = {self.current_term: data['candidate_id']}
                # persist changes
                node.storage.persist(self)
                return self.vote_response_message(node, data['candidate_id'], True)

        return self.vote_response_message(node, data['candidate_id'], False)

    def on_vote_response(self, node, msg):
        """
        This is called when there is a vote response.

        :param node: Node receiving vote response
        :param msg: The vote response message
        :type node: pyraftlog.node.Node
        :type msg: pyraftlog.message.Message
        :return: Response message
        :rtype: pyraftlog.message.Message
        """
        # If we are not a candidate ignore
        if self.mode != STATE_MODE_CANDIDATE:
            return None

        # Ignore messages from previous terms
        if msg.term < self.current_term:
            node.log(logging.ERROR, 'Ignoring %s', msg)
            return None

        node.log(logging.DEBUG, 'Received vote from %s: %r', msg.sender, msg.data['response'])
        # Update the votes tally
        self.votes[msg.sender] = msg.data['response']

        # If we have successfully received a majority
        if node.has_majority(self.votes.values().count(True)):
            # Promote yourself to leader
            node.log(logging.CRITICAL, 'Converting to Leader (Log index: %s)', self.log)
            self.mode = STATE_MODE_LEADER
            node.synchronised = dict.fromkeys(node.neighbours, False)
            node.reset_timeout()

            return None

        else:
            if self.votes.values().count(True) == 1 and self.votes.values().count(False) >= 1:
                return None

            return None

    def on_append_entries(self, node, msg):
        """
        This is called when there is a request to append an entry to the log.

        :param node: Node receiving request
        :param msg: The append entries message
        :type node: pyraftlog.node.Node
        :type msg: pyraftlog.message.Message
        :return: Response message
        :rtype: pyraftlog.message.Message
        """
        data = msg.data

        # If we are not a Follower
        if self.mode != STATE_MODE_FOLLOWER:
            self.mode = STATE_MODE_FOLLOWER

        # Reply false if the message term < our current term
        if msg.term < self.current_term:
            node.log(logging.INFO, 'This Node is ahead of the sender term (%2d < %2d)', msg.term, self.current_term)
            return self.append_response_message(node, msg.sender, False, 'Sender term is outdated')

        # Fail fast if prev log index has been reduced
        if (self.log.tail().index - 1) > data['prev_log_index']:
            node.log(logging.WARN, 'Logs have been reduced: %d > %d', self.log.tail().index, data['prev_log_index'])
            return self.append_response_message(node, msg.sender, False, 'Logs have been reduced')

        # Can't be up to date if our log is smaller than prev log index
        if self.log.index() < data['prev_log_index']:
            node.log(logging.INFO, 'This Node is behind the log index (%2d < %2d)',
                     self.log.index(), data['prev_log_index'])
            return self.append_response_message(node, msg.sender, False, 'Log is further behind')

        # If our term doesn't match the leaders
        if self.log.get(data['prev_log_index']).term != data['prev_log_term']:
            entry = self.log.get(data['prev_log_index'])
            node.log(logging.WARN, 'This Node has inconsistent logs (%2d,%2d) != (%2d,%2d)',
                     entry.term, entry.index, data['prev_log_term'], data['prev_log_index'])
            if self.log.tail().index <= data['prev_log_index']:
                self.log.rewind(data['prev_log_index'] - 1)
            return self.append_response_message(node, msg.sender, False, 'Inconsistent logs')

        # The induction proof held so we append any new entries
        for index, e in enumerate(data['entries'], data['prev_log_index'] + 1):
            node.log(logging.INFO, 'Considering entry: (%2d,%2d)', e[0], e[1])
            # If an existing entry conflicts with a new one trust the leaders log
            if self.log.index() >= index and self.log.get(index).term != e[0]:
                entry = self.log.get(index)
                node.log(logging.WARN, 'This Node has inconsistent logs (%2d,%2d) != (%2d,%2d)',
                         entry.term, entry.index, e[0], e[1])
                if self.log.tail().index <= data['prev_log_index']:
                    self.log.rewind(index - 1)

            # Append any new entries not already in the log
            if self.log.index() < index:
                node.log(logging.WARN, '"Appending entry to log at index %2d', e[1])
                self.log.append(e[0], e[2])

        # Update our commit index
        if data['leader_commit'] > self.commit_index:
            self.commit_index = min(data['leader_commit'], self.log.index())
            node.apply_event.set()

            # Update our cluster_applied and log reduction
            self.cluster_applied = data['cluster_applied']
            self.log_reduction = data['log_reduction']
        # Reduce the log
        if self.log_reduction:
            if self.log.reduce(min(self.cluster_applied.values())):
                node.log(logging.DEBUG, 'Reduced log to %2d', len(self.log))

        # persist changes
        node.storage.persist(self)

        return self.append_response_message(node, msg.sender, True, 'Appended' if len(data['entries']) else 'Heartbeat')

    def on_append_response(self, node, msg):
        """
        This is called when there is a append entries response.

        :param node: Node receiving request
        :param msg: The append entries response message
        :type node: pyraftlog.node.Node
        :type msg: pyraftlog.message.Message
        :return: Response message
        :rtype: pyraftlog.message.Message
        """
        if self.mode != STATE_MODE_LEADER:
            return None

        data = msg.data
        # Mark message sender as in/out of sync
        node.synchronised[msg.sender] = data['response']
        if not data['response']:
            # Attempt to catch up the node that is behind
            if self.log.head().index > 0:
                # Default to stepping back through the log by one
                self.next_index[msg.sender] = max(0, self.log.prev_index(self.next_index[msg.sender]))

                # If we think their next index is 0 or they think their last appended is less than next index
                if self.next_index[msg.sender] == 0 or data['last_appended'] < self.next_index[msg.sender]:
                    # Use their last appended to speed up recovery
                    self.next_index[msg.sender] = self.log.next_index(data['last_appended'])

                # If their next index is less than our log tail we have a serious issue!
                if self.next_index[msg.sender] < self.log.tail().index:
                    node.log(logging.CRITICAL, '%s next index is no longer available', msg.sender)

                # If next index is the tail increment their next index by one
                if self.next_index[msg.sender] == self.log.tail().index:
                    self.next_index[msg.sender] += 1

        else:
            # Update the match next indexes for the message sender
            self.match_index[msg.sender] = min(self.log.index(), self.next_index[msg.sender])
            self.next_index[msg.sender] = min(self.log.index() + 1, self.log.next_index(data['last_appended']))

            # Update commit index if there is a majority
            for index in sorted(self.match_index.values(), reverse=True):
                if index > self.commit_index:
                    count = sum(1 for x in self.match_index.values() if x >= index)
                    if node.has_majority(count + 1):
                        node.log(logging.WARN, 'Committed log to index (%2d)', index)
                        self.commit_index = index
                        node.apply_event.set()
                        self.statistics.set_committed_timestamp(self.commit_index, time.time())
                        # persist changes
                        node.storage.persist(self)

            # Update `cluster_applied`
            self.cluster_applied[msg.sender] = data['last_applied']

        # Perform log reduction
        if self.log_reduction:
            if self.log.reduce(min(self.cluster_applied.values())):
                node.log(logging.DEBUG, 'Reduced log to %2d', len(self.log))
                # persist changes
                node.storage.persist(self)

        return None

    def append_log_entry(self, command):
        """
        Create a new log entry with `command` and append it to the log.

        :param command: Command to be performed
        :type command: Any
        :return: The index of the created entry
        :rtype: int|False
        """
        if self.mode != STATE_MODE_LEADER:
            return False

        index = self.log.append(self.current_term, command)
        self.statistics.set_append_timestamp(index, time.time())

        return index

    def vote_request_message(self, candidate, recipient):
        """
        Generate a vote request message for `recipient`.

        :param candidate: Candidate node
        :param recipient: Neighbour that will receive the message
        :type candidate: pyraftlog.node.Node
        :type recipient: str
        :return: A vote request message
        :rtype: pyraftlog.message.Message
        """
        return message.Message.build(message.VOTE_REQUEST, candidate, self, recipient, {
            "candidate_id": candidate.name,
            "last_log_index": self.log.index(),
            "last_log_term": self.log.head().term if self.log else 0,
        })

    def vote_response_message(self, voter, candidate, response):
        """
        Generate a vote response message for `candidate`.

        :param voter: Consensus node voting
        :param candidate: Neighbour that will receive the message
        :param response: Whether the candidate received your vote
        :type voter: pyraftlog.node.Node
        :type candidate: str
        :type response: bool
        :return: A vote response message
        :rtype: pyraftlog.message.Message
        """
        return message.Message.build(message.VOTE_RESPONSE, voter, self, candidate, {
            "response": response
        })

    def append_entry_message(self, leader, recipient, heartbeat=False):
        """
        Generate an append entry message for `recipient`.

        :param leader: Leader node
        :param recipient: Neighbour that will receive the message
        :param heartbeat: Whether this is a heartbeat message
        :type leader: pyraftlog.node.Node
        :type recipient: str
        :type heartbeat: bool
        :return: An append entries message
        :rtype: pyraftlog.message.Message
        """
        next_log_index = self.next_index[recipient]
        prev_log_index = self.log.prev_index(next_log_index)
        synchronised = leader.synchronised[recipient]
        entries = [] if heartbeat or not synchronised else self.log.chunk(next_log_index, CHUNK_SIZE, MAX_CHUNK_BYTES)

        return message.Message.build(message.APPEND_ENTRIES, leader, self, recipient, {
            "leader_id": leader.name,
            "prev_log_index": prev_log_index,
            "prev_log_term": self.log.get(prev_log_index).term,
            "entries": entries,
            "leader_commit": self.commit_index,

            # Inform followers of request address for clients
            "request_address": leader.request_address,

            # Inform followers of whether log reduction is active
            # and where the whole cluster is up to
            "log_reduction": self.log_reduction,
            "cluster_applied": self.cluster_applied,
        })

    def append_response_message(self, follower, recipient, response, reason):
        """
        Generate an append entry response for `recipient`.

        :param follower: Follower node
        :param recipient: Neighbour that will receive the message
        :param response: Whether the append entry message was accepted
        :param reason: Reason for the response
        :type follower: pyraftlog.node.Node
        :type recipient: str
        :type response: bool
        :type reason: str
        :return: An append entries response message
        :rtype: pyraftlog.message.Message
        """
        return message.Message.build(message.APPEND_RESPONSE, follower, self, recipient, {
            "response": response,
            "reason": reason,
            "last_applied": self.last_applied,

            # Inform the leader the head of our log
            "last_appended": self.log.index(),
        })
