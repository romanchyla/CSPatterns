from collections import defaultdict


class UnionFind(object):
    """Impl of UnionFind with O(logN) find operation;
    we are keeping track of the size of the underlying
    branches; making them balanced. This class can use
    any values for a key (internally is mapped to ints)
    but we are doing no compression. Maybe later..."""

    def __init__(self, values=None):
        self._map = defaultdict(int)
        self._data = []
        self._size = []
        self._num_components = 0

        if values:
            for v in values:
                self.get_key(v)
        # print(self._map, self._data, self._size, self._num_components)

    def get_key(self, v):
        key = self._map.get(v, len(self._map))
        if key == len(self._data):
            self._data.append(key)
            self._map[v] = key
            self._size.append(1)
            self._num_components += 1
        return key

    def find(self, v):
        parent = self.get_key(v)
        data = self._data

        while data[parent] != parent:
            parent = data[parent]
        return parent

    def join(self, v, w):
        parentv = self.find(v)
        parentw = self.find(w)

        if parentv == parentw:
            return

        # connect the smaller to the bigger - that way
        # we are making sure that the tree height is
        # staying minimal (if we were to connect bigger
        # to smaller we are doing the opposite - growing
        # tree height)
        if self._size[parentv] > self._size[parentw]:
            parentv, parentw = parentw, parentv

        self._data[parentv] = parentw
        self._size[parentw] += self._size[parentv]
        self._num_components -= 1

    def is_connected(self, v, w):
        return self.find(v) == self.find(w)

    def num_components(self) -> int:
        """Return number of distinct components"""
        return self._num_components

    def size(self):
        return len(self._data)

    def compress(self):
        for i, v in enumerate(self._data):
            p = self.find(v)
            self._data[i] = p
        return self._data
