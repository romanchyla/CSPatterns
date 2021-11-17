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
        print(self._map, self._data, self._size, self._num_components)

    def get_key(self, v):
        key = self._map.get(v, len(self._map))
        if key == len(self._data):
            self._data.append(key)
            self._map[v] = key
            self._size.append(1)
            self._num_components += 1
        return key

    def get_parent(self, v):
        parent = self.get_key(v)
        data = self._data

        while data[parent] != parent:
            parent = data[parent]
        return parent

    def join(self, v, w):
        parentv = self.get_parent(v)
        parentw = self.get_parent(w)

        if parentv == parentw:
            return
        
        if self._size[parentv] > self._size[parentw]:
            parentv, parentw = parentw, parentv

        self._data[parentv] = parentw
        self._size[parentw] += self._size[parentv]
        self._num_components -= 1

    
    def is_connected(self, v, w):
        return self.get_parent(v) == self.get_parent(w)


    def num_components(self) -> int:
        """Return number of distinct components"""
        return self._num_components


    def size(self):
        return len(self._data)