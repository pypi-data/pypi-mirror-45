import msgpack
import threading
from collections import namedtuple

Entry = namedtuple('Entry', 'term index value')
empty = Entry(0, 0, None)


class Log(object):
    """
    This class logs the history of commands appended to the consensus node.
    """

    def __init__(self, iterable=()):
        """
        :param iterable: An iterable set of entries
        :type iterable: iterable
        """
        self.entries = list(iterable)
        self.lock = threading.Lock()
        self.cindex = self.entries[-1].index if self.entries else 0
        self.offset = self.entries[0].index - 1 if self.entries else 0

    def __setstate__(self, state):
        self.__dict__.update(state)
        self.lock = threading.Lock()

    def __getstate__(self):
        state = self.__dict__.copy()
        del state['lock']
        return state

    def __len__(self):
        return len(self.entries)

    def __str__(self):
        return "%d,%d" % (self.head().term, self.head().index)

    def index(self):
        """
        :return: Latest index in the log
        :rtype: int
        """
        return self.cindex

    def get(self, idx):
        """
        :param idx: Index of entry to get
        :type idx: int
        :return: The Entry with the index `idx`
        :rtype: Entry
        """
        return self.entries[idx - (1 + self.offset)] if self.contains(idx) else empty

    def slice(self, idx, size=None):
        """
        :param idx: from index
        :param size: number of elements to include (up to)
        :type idx: int
        :type size: int
        :return: A slice of the entries in the log
        :rtype: list[Entry]
        """
        i = max(0, idx - (1 + self.offset))
        if size is None:
            return self.entries[i:]
        else:
            j = min(self.cindex, i) + size
            return self.entries[i:j]

    def chunk(self, idx, chunk_size, max_chunk_bytes):
        """
        Get a chunk of log entries starting from `idx` limited in size by the log size, `chunk_size`,
        or `max_chunk_bytes`.
        Return a minimum of one entry.

        :param idx: Starting position
        :param chunk_size: Maximum number of entries
        :param max_chunk_bytes: Maximum number of bytes
        :type idx: int
        :type chunk_size: int
        :type max_chunk_bytes: int
        :return:
        :rtype: (int, str)
        """
        chunk_entries = []
        size, entry_count = 0, 0
        for entry in self.slice(idx):
            cur_size = len(msgpack.dumps(entry.__dict__))

            # Chunk at least one entry, chunk if this new entry breaks either bytes or length limit
            if chunk_entries and (size + cur_size > max_chunk_bytes) or entry_count == chunk_size:
                return chunk_entries

            chunk_entries.append(entry)
            size += cur_size
            entry_count += 1

        return chunk_entries

    def contains(self, idx):
        """
        :param idx: Index
        :type idx: int
        :return: True if the index is still in the Log, False otherwise
        :rtype: Entry
        """
        return self.offset < idx <= self.cindex

    def head(self):
        """
        :return: Most recently appended `Entry`
        :rtype: Entry
        """
        return self.entries[-1] if self.entries else empty

    def tail(self):
        """
        :return: Least recently appended `Entry` (that has not been reduced away)
        :rtype: Entry
        """
        return self.entries[0] if self.entries else empty

    def prev_index(self, index):
        """
        :param index: index to find previous from
        :type index: int
        :return: Previous index from `index`
        :rtype: int
        """
        if self.cindex < index:
            return self.cindex
        if self.contains(index - 1):
            return index - 1
        else:
            return 0

    def next_index(self, index=None):
        """
        :param index: index to find next from
        :type index: int
        :return: Next index after `index`
        :rtype: int
        """
        if index is None:
            return self.cindex + 1

        if self.contains(index):
            return index + 1
        elif index > self.cindex:
            return self.cindex + 1
        else:
            return self.offset + 1

    def values(self, i, j):
        """
        :param i: from index
        :param j:
        :type i: int
        :type j: to index
        :return: List of all log values from `i` to `j`
        :rtype: list[dict[str, Any]]
        """
        i = max(self.offset, i - 1) - self.offset
        j = min(self.cindex, j) - self.offset
        return [{"term": e.term, "index": e.index, "value": e.value} for e in self.entries[i:j]]

    def append(self, term, value):
        """
        :param term: Term this value is being appended in
        :param value: Value to be stored in the `Entry`
        :type term: int
        :type value: Any
        :return: Index of the appended `Entry`
        :rtype: int
        """
        with self.lock:
            self.cindex += 1
            self.entries.append(Entry(term, self.cindex, value))
            return self.cindex

    def reduce(self, index):
        """
        Remove all entries in the log with an index less than `index`.

        :param index: Index to reduce to
        :type index: int
        :return: True if log effected
        :rtype: bool
        """
        with self.lock:
            current_size = len(self.entries)

            if index > self.cindex:
                self.entries = []
                self.offset = index
                self.cindex = index
            else:
                index = max(0, (min(index, self.cindex) - 1) - self.offset)
                self.entries = self.entries[index:]
                self.offset = self.entries[0].index - 1 if self.entries else 0

            return current_size != len(self.entries)

    def rewind(self, index):
        """
        Remove all entries in the log with an index greater than `index`.

        :param index: Index
        :type index: int
        :return: True if log effected
        :rtype: bool
        """
        with self.lock:
            current_size = len(self.entries)

            if index <= self.offset:
                self.entries = []
                self.offset = index
                self.cindex = index
            else:
                index = max(index + 1, self.offset)
                self.entries = self.entries[:index - (1 + self.offset)]
                self.cindex = self.entries[-1].index if self.entries else 0

            return current_size != len(self.entries)
