from collections import defaultdict, deque

from cspatterns.datastructures import unionfind


def postorder_dfs(graph):
    seen = set()
    out = []
    weighted = isinstance(graph, WeightedUndirectedGraph) or isinstance(
        graph, WeightedDirectedGraph
    )

    def dfs(v, graph, out):
        if v in seen:
            return
        seen.add(v)
        for w in graph.adj(v):
            if weighted:
                w = w[0]
            if w not in seen:
                dfs(w, graph, out)
        out.append(v)

    for v in graph.vertices():
        if v not in seen:
            dfs(v, graph, out)
    return out


def postorder_iter(graph):
    """Returns stack with the element on top
    of the stack to be examined first."""
    stack = []
    seen = set()
    out = []
    weighted = isinstance(graph, WeightedDirectedGraph) or isinstance(
        graph, WeightedUndirectedGraph
    )
    for v in graph.vertices():
        if v not in seen:
            stack.append((v, False))
            while stack:
                x, xdone = stack.pop()
                if xdone:
                    out.append(x)
                elif x not in seen:
                    stack.append((x, True))
                    seen.add(x)
                    # probably slight perf hit but will produce
                    # the same order as recursive DFS
                    if weighted:
                        for w in reversed([w for w, _ in graph.adj(x)]):
                            stack.append((w, False))
                    else:
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

    def has_vertex(self, v) -> bool:
        return v in self._src

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
            x += 1
        self.E -= max(min(x, 1), 0)

    def vertices(self) -> object:
        for k in self._src.keys():
            yield k

    def edges(self) -> object:
        for v in self.vertices():
            for w in DirectedGraph.adj(self, v):
                yield (v, w)

    def num_vertices(self) -> int:
        return len(self._src)

    def num_edges(self) -> int:
        return self.E

    def adj(self, v) -> object:
        if v in self._src:
            for w in self._src[v]:
                yield w

    def reverse(self):
        grev = self.__class__()
        for v, w in self.edges():
            grev.add(w, v)
        return grev

    def topological_sort(self):
        """Returns items in left-right order;
        so that position of f(v) < f(w). In other
        words 1->2->3 should produce [1, 2, 3]
        """
        stack = postorder_iter(self)
        while stack:
            yield stack.pop()

    def find_strongly_connected_components(self):
        """
        Strongly connected component is basically
        a cycle (any vertex inside SCC can be reached
        starting from any other vertex inside SCC)

        This function will thus identify all SCCs and
        turn the directed graph into DAG; even if there
        were any cycles (SCCs) inside.

        We use Kosaraju topological sort to identify strongly
        connected components and take care to use iterative
        approach (instead of recursion) in case we have
        to deal with large graphs

        I got this not exactly right several times, so here
        is explanation for my future self:

        The main goal is to identify *sink* vertices - and
        collect connected components from the end (from sinks). If
        we do post-order DFS on the graph itself, we are
        not guaranteed to always identify the sink vertex.
        Because the DFS will recurse and may end up going into
        a shorter (blind) path which does not reach the real
        last connected component. Because we go to the end,
        these vertices will be emitted first for consideration.

        And that is a problem because it means that we can
        lump two SCC together, or have CC in inproper order.

        But post-order DFS is guaranteed to always identify source
        vertices. I.e. imagine DAG, with v->w path: because
        we are exploring the graph randomly (for each vertex)
        there are two options:

        (w)
        Either we hit 'w' first, which will assign 'w' higher
        topological order. When we (eventually) get to explore
        'v' (w was already visited) 'v' will have topological
        smaller order. So 'v' is on left of w.

        (v)
        In case when we hit 'v' first; because of the post-order
        DFS we end up assigning 'w' higher topological order
        (precisely because of post-order DFS descends into w
        before processing v).

        So either way: the starting vertices (source) are going
        to be properly ordered.

        For getting connected components; we desire to identify
        'sink' components and start exploring the graph from the
        end. Since we can identify 'sources' reliably, the solution
        is to reverese the graph first; then run post-order DFS
        on G_rev in order to find 'sources' of Grev. (sources of
        G_rev are the same thing as true 'sinks' of the original
        graph)

        So if we got sinks of G; we can then reliably collect
        connected components - because whatever we do, whichever
        cycle we may enter, we are chopping of parts of the graph
        from right.


        @return: List[int, [int, int], ....]
                the nested list identifies cycles
        """

        # iterator into sink vertices
        sinks = self.reverse().topological_sort()

        visited = set()  # for when we are finished
        dfs_stack = []
        out = deque()
        weighted = isinstance(self, WeightedUndirectedGraph) or isinstance(
            self, WeightedDirectedGraph
        )

        for v in sinks:
            if v not in visited:
                pointer = deque()
                dfs_stack.append((v, False))

                while dfs_stack:
                    v, vdone = dfs_stack.pop()
                    # print(v, vdone)
                    if vdone:  # post-order return
                        pointer.appendleft(v)
                    else:
                        if v not in visited:
                            visited.add(v)
                            dfs_stack.append((v, True))
                            for w in self.adj(v):
                                if weighted:
                                    w = w[0]
                                if w not in visited:
                                    dfs_stack.append((w, False))
                if len(pointer) > 1:  # only happens for cycles
                    out.appendleft(list(pointer))
                else:
                    out.appendleft(pointer[0])
        # print('result', out)
        return list(out)


class WeightedDirectedGraph(DirectedGraph):
    def __init__(self, *args, **kwargs):
        self._weights = {}
        self._total_weight = 0.0
        super().__init__(*args, **kwargs)

    def add(self, v, w, weight):
        super().add(v, w)
        key = self._key(v, w)
        self._total_weight = self._total_weight - self._weights.get(key, 0) + weight
        self._weights[key] = weight

    def delete(self, v, w):
        super().delete(v, w)
        key = self._key(v, w)
        weight = self._weights[key]
        del self._weights[key]
        self._total_weight -= weight

    def edges(self):
        for v, w in super().edges():
            yield (v, w, self._weights[(v, w)])

    def adj(self, v):
        for w in super().adj(v):
            key = self._key(v, w)
            yield (w, self._weights[key])

    def total_weight(self) -> float:
        return self._total_weight

    def update_weight(self, v, w, weight):
        key = self._key(v, w)
        if key not in self._weights:
            raise Exception("The edge {} is not present", key)
        self._total_weight = self._total_weight - self._weights.get(key, 0) + weight
        self._weights[key] = weight

    def get_weight(self, v, w, default=None) -> float:
        key = self._key(v, w)
        if key in self._weights:
            return self._weights[key]
        else:
            if default is None:
                raise Exception("The edge {} is not present", key)
            else:
                return default

    def reverse(self):
        grev = self.__class__()
        for v, w, weight in self.edges():
            grev.add(w, v, weight)
        return grev


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

    def has_vertex(self, v) -> bool:
        return v in self._src

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
            x += 1
        if w in self._src and v in self._src[w]:
            self._src[w].remove(v)
            if len(self._src[w]) == 0:
                del self._src[w]
            x += 1

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
            for w in self._src[v]:
                yield w
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
        super().add(v, w)
        key = self._key(v, w)
        self._total_weight = self._total_weight - self._weights.get(key, 0) + weight
        self._weights[key] = weight

    def delete(self, v, w):
        super().delete(v, w)
        key = self._key(v, w)
        weight = self._weights[key]
        del self._weights[key]
        self._total_weight -= weight

    def edges(self):
        for v, w in super().edges():
            yield (v, w, self._weights[(v, w)])

    def adj(self, v):
        for w in super().adj(v):
            key = self._key(v, w)
            yield (w, self._weights[key])

    def total_weight(self) -> float:
        return self._total_weight

    def update_weight(self, v, w, weight):
        key = self._key(v, w)
        if key not in self._weights:
            raise Exception("The edge {} is not present", key)
        self._total_weight = self._total_weight - self._weights.get(key, 0) + weight
        self._weights[key] = weight

    def get_weight(self, v, w, default=None) -> float:
        key = self._key(v, w)
        if key in self._weights:
            return self._weights[key]
        else:
            if default is None:
                raise Exception("The edge {} is not present", key)
            else:
                return default
