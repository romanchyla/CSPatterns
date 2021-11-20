from collections import defaultdict
from cspatterns.datastructures import unionfind

class Node(object):
    def __init__(self, val, left=None, right=None) -> None:
        self.val = val
        self.left = left
        self.right = right


class UndirectedGraph(object):
    """
    Undirected graph using adjacency list
    """
    def __init__(self, *edges):
        self._edges = defaultdict(set)
        self.E = 0
        for edge in edges:
            self.add(*edge)

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

    def delete(self, v, w):
        x = 0
        if v in self._edges and w in self._edges[v]:
            self._edges[v].remove(w)
            if len(self._edges[v]) == 0:
                del self._edges[v]
            x +=1
        if w in self._edges and v in self._edges[w]:
            self._edges[w].remove(v)
            if len(self._edges[w]) == 0:
                del self._edges[w]
            x +=1
        
        self.E -= max(min(x, 1), 0)


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

    def find_connected_components(self):
        uf = unionfind.UnionFind(values=self.vertices())
        for e in self.edges():
            uf.join(e[0], e[1])
        uf.compress()
        ccs = defaultdict(list)
        for e in self.edges():
            ccs[uf.find(e[0])].append(e)
        return list(ccs.values())

class WeightedUndirectedGraph(UndirectedGraph):
    def __init__(self, *args, **kwargs):
        self._weights = {}
        self._total_weight = 0.0
        super().__init__(*args, **kwargs)

    def add(self, v, w, weight):
        super().add(v,w)
        key = self._key(v,w)
        self._total_weight = self._total_weight - self._weights.get(key, 0) + weight
        self._weights[key] = weight

    def delete(self, v, w):
        super().delete(v,w)
        key = self._key(v,w)
        weight = self._weights[key]
        del self._weights[key]
        self._total_weight -= weight
    
    def edges(self):
        for v,w in super().edges():
            yield (v, w, self._weights[(v,w)])
    
    def adj(self, v):
        for w in super().adj(v):
            key = self._key(v, w)
            yield (w, self._weights[key])

    def total_weight(self) -> float:
        return self._total_weight

    def update_weight(self, v, w, weight):
        key = self._key(v,w)
        if key not in self._weights:
            raise Exception('The edge {} is not present', key)
        self._total_weight = self._total_weight - self._weights.get(key, 0) + weight
        self._weights[key] = weight

    def get_weight(self, v, w, default=None) -> float:
        key = self._key(v,w)
        if key in self._weights:
            return self._weights[key]
        else:
            if default is None:
                raise Exception('The edge {} is not present', key)
            else:
                return default