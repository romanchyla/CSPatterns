from collections import defaultdict

class Node(object):
    def __init__(self, val, left=None, right=None) -> None:
        self.val = val
        self.left = left
        self.right = right


class UndirectedGraph(object):
    """
    Undirected graph using adjacency list
    """
    def __init__(self):
        self._edges = defaultdict(set)
        self.E = 0

    def _key(self, v, w):
        if v <= w:
            return (v, w)
        else:
            return (w, v)
    
    def has(self, v, w) -> bool:
        return v in self._edges and self._edges[v].get(w, False)

    def add(self, v, w):
        old_v = len(self._edges[v])
        old_w = len(self._edges[w])

        self._edges[v].add(w)
        self._edges[w].add(v)

        self.E += (len(self._edges[v]) - old_v + len(self._edges[w]) - old_w) // 2

    def vertices(self) -> object:
        if self.E:
            for k in self._edges.keys():
                yield k
        else:
            raise StopIteration

    def edges(self) -> object:
        seen = set()
        for v in self.vertices():
            for w in UndirectedGraph.adj(self, v):
                key = self._key(v, w)
                if key in seen:
                    continue
                yield key
                seen.add(key)

    def num_vertices(self) -> int:
        return len(self._edges)

    def num_edges(self) -> int:
        return self.E

    def adj(self, v) -> object:
        if v in self._edges:
            for x in self._edges[v]:
                yield x
        else:
            raise StopIteration

class WeightedUndirectedGraph(UndirectedGraph):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._weights = {}
        self._total_weight = 0.0

    def add(self, v, w, weight):
        super().add(v,w)
        key = self._key(v,w)
        self._total_weight = self._total_weight - self._weights.get(key, 0) + weight
        self._weights[key] = weight
        
    
    def edges(self):
        for v,w in super().edges():
            yield (v, w, self._weights[(v,w)])
    
    def adj(self, v):
        for w in super().adj(v):
            key = self._key(v, w)
            yield (w, self._weights[key])

    def total_weight(self) -> float:
        return self._total_weight
