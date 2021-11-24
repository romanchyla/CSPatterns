from collections import defaultdict, deque
from cspatterns.datastructures import unionfind

def postorder_dfs(graph):
    seen = set()
    out = []
    def dfs(v, graph, out):
        if v in seen:
            return
        seen.add(v)
        for w in graph.adj(v):
            if w not in seen:
                dfs(w, graph, out)
        out.append(v)
    for v in graph.vertices():
        if v not in seen:
            dfs(v, graph, out)
    return out

def postorder_iter(graph):
    stack = []
    seen = set()
    out = []
    for v in graph.vertices():
        if v not in seen:
            stack.append((v, False))
            while stack:
                x,xdone = stack.pop()
                if xdone:
                    out.append(x)
                elif x not in seen:
                    stack.append((x, True))
                    seen.add(x)
                    # probably slight perf hit but will produce
                    # the same order as recursive DFS
                    for w in reversed(list(graph.adj(x))):
                        stack.append((w, False))
    return out
  

class DirectedGraph(object):
    """
    DG using adjacency list
    """
    def __init__(self, *edges):
        self._src = defaultdict(set)
        self.E = 0
        for edge in edges:
            self.add(*edge)

    def _key(self, v, w):
        return (v, w)
    
    def has(self, v, w) -> bool:
        return v in self._src and self._src[v].get(w, False)

    def add(self, v, w):
        old_v = len(self._src[v])
        self._src[v].add(w)
        self.E += len(self._src[v]) - old_v

        if w not in self._src:
            self._src[w]


    def delete(self, v, w):
        x = 0
        if v in self._src and w in self._src[v]:
            self._src[v].remove(w)
            if len(self._src[v]) == 0:
                del self._src[v]
            x +=1
        self.E -= max(min(x, 1), 0)


    def vertices(self) -> object:
        for k in self._src.keys():
            yield k

    def edges(self) -> object:
        for v in self.vertices():
            for w in self.adj(v):
                yield (v, w)

    def num_vertices(self) -> int:
        return len(self._src)

    def num_edges(self) -> int:
        return self.E

    def adj(self, v) -> object:
        if v in self._src:
            for x in self._src[v]:
                yield x
        

    def reverse(self):
        grev = DirectedGraph()
        for v,w in self.edges():
            grev.add(w, v)
        return grev

    def topological_sort(self):
        return postorder_iter(self)          


    def find_connected_components(self):
        """
        Kosaraju topological sort to identify strongly
        connected components; even if the graph may 
        contain cycles. We take care to use iterative
        approach (instead of recursion) in case we have
        to deal with large graphs


        @return: List[int, [int, int], ....]
                the nested list identifies cyclic connected 
                components
        """

        grev = self.reverse()
        ts = grev.topological_sort()

        print('ts', ts)
        seen = set()
        dfs_stack = []
        pointer = deque()
        

        for v in ts:
            if v not in seen:
                cycle_end, cycle_start = [(float('inf'), float('inf'))], [-1]
                cycle_stack = []
                dfs_stack = [v]

                while dfs_stack:
                    while dfs_stack[-1] not in seen:
                        x = dfs_stack[-1]
                        for w in self.adj(x):
                            if w in seen: # cycle detected
                                cycle_end.append((w, x))
                                print('cycle x={} w={}'.format(x, w))
                            else:
                                dfs_stack.append(w)
                        seen.add(x)
                        
                    v = dfs_stack.pop()
                    start, end = cycle_start[-1], cycle_end[-1][1]                       
                    print('v={} start={} end={} '.format(v, start, end))

                    if v == end: # go to deeper level (nested cycle)
                        while cycle_end[-1][1] == end:
                            cycle_stack.append(pointer)
                            pointer = deque()
                            cycle_start.append(cycle_end.pop()[0])
                        pointer.appendleft(v)
                        cycles_found = True
                    elif v == start: # exit this level (cycle)
                        pointer.appendleft(v)
                        while cycle_start[-1] == start:
                            cycle_stack[-1].appendleft(pointer)
                            pointer = cycle_stack.pop()
                            cycle_start.pop()
                    else:
                        pointer.appendleft(v)
                
                        
        return pointer
            




class UndirectedGraph(object):
    """
    Undirected graph using adjacency list
    """
    def __init__(self, *edges):
        self._src = defaultdict(set)
        self.E = 0
        for edge in edges:
            self.add(*edge)

    def _key(self, v, w):
        if v <= w:
            return (v, w)
        else:
            return (w, v)
    
    def has(self, v, w) -> bool:
        return v in self._src and self._src[v].get(w, False)

    def add(self, v, w):
        old_v = len(self._src[v])
        old_w = len(self._src[w])

        self._src[v].add(w)
        self._src[w].add(v)

        self.E += (len(self._src[v]) - old_v + len(self._src[w]) - old_w) // 2

    def delete(self, v, w):
        x = 0
        if v in self._src and w in self._src[v]:
            self._src[v].remove(w)
            if len(self._src[v]) == 0:
                del self._src[v]
            x +=1
        if w in self._src and v in self._src[w]:
            self._src[w].remove(v)
            if len(self._src[w]) == 0:
                del self._src[w]
            x +=1
        
        self.E -= max(min(x, 1), 0)


    def vertices(self) -> object:
        if self.E:
            for k in self._src.keys():
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
        return len(self._src)

    def num_edges(self) -> int:
        return self.E

    def adj(self, v) -> object:
        if v in self._src:
            for x in self._src[v]:
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