from collections import defaultdict, deque


class Floyd(object):
    """
    All pairs shortest paths with negative weights allowed
    (but no negative cycles)

    time: O(V^3)
    space: O(V^2) -- with high constant; as we are keeping 2*V
           with just mappings from vertex labels back to internal
           ints (dp); which sucks
    """

    def __init__(self, graph) -> None:
        super().__init__()
        self.graph = graph
        self._find_shortest_paths()

    def _find_shortest_paths(self):

        # the graph can contain arbitrary labels (not only ints)
        # and since some of them could have been deleted we can't
        # rely on the internal int representation; we could have
        # used map directly - but this will be somewhat better for
        # large graphs (maybe)
        V = 0
        dmap = {}
        imap = {}
        for v in self.graph.vertices():
            dmap[v] = V
            imap[V] = v
            V += 1

        dp = [[float("inf")] * V for _ in range(V)]
        parent = list(range(V))

        for v in range(V):
            dp[v][v] = 0

        for v, w, weight in self.graph.edges():
            dp[dmap[v]][dmap[w]] = weight
            parent[dmap[w]] = parent[dmap[v]]

        for k in range(V):
            for v in range(V):
                if v == k or dp[v][k] == float("inf"):
                    continue
                for w in range(V):
                    weight = dp[v][k] + dp[k][w]
                    if weight < dp[v][w]:
                        dp[v][w] = weight
                        parent[w] = k

        self._v2imap = dmap
        self._i2vmap = imap
        self._parent = parent
        self._distances = dp

    def get_distance_between(self, v, w):
        iv = self._v2imap.get(v, -1)
        iw = self._v2imap.get(w, -1)
        if iw == -1 or iv == -1:
            return None  # one of the vertices is not from the graph
        return self._distances[iv][iw]

    def get_path_between(self, v, w):
        d = self.get_distance_between(v, w)
        if d is None or d == float("inf"):
            return []

        out = deque()
        i2vmap = self._i2vmap
        iv = self._v2imap[v]
        t = self._v2imap[w]
        while t != self._parent[t] and t != iv:
            out.appendleft(i2vmap[t])
            t = self._parent[t]
        out.appendleft(v)
        return list(out)

    def get_path_to(self, w):
        if not self.graph.has_vertex(w):
            return []

        out = deque()
        t = self._v2imap[w]
        i2vmap = self._i2vmap

        while t != self._parent[t]:
            out.appendleft(i2vmap[t])
            t = self._parent[t]
        out.appendleft(i2vmap[t])
        return list(out)


class BellmannFord(object):
    """
    Find single source shortest path to every vertex in the
    graph. We allow negative weights, but negative cycles will raise
    exception (positive cycle will not cause it). Negative cycle
    means we'd enter into a loop that we can't exit.

    time: O(E*V)
    """

    def __init__(self, graph, source) -> None:
        super().__init__()
        self.source = source
        self.graph = graph

        if not graph.has_vertex(source):
            raise Exception("Source vertex {} is missing from the graph".format(source))

        self._find_shortest_paths()

    def _find_shortest_paths(self):
        """
        Nature of Bellmann-Ford is that we keep growing
        path from the source one element at a time. There
        are *at most* |V|-1 edges from the source to any
        other vertex. And DP algorithm will keep growing
        them one edge at a time. If we have explored all
        vertices and the distances have not stabilized, then
        we know there must exist a negative cycle (somewhere)
        """

        # have to use dict because the graph can contain arbitrary vertices
        # otherwise we'd have to force them to be ints
        dst_to = defaultdict(lambda: float("inf"))
        dst_to[self.source] = 0
        parent = {self.source: None}

        for _ in self.graph.vertices():
            # WRONG! we must run the cycle V times (ONE MORE TIME than necessary)
            # if we were to successfuly detect every negative cycle
            # if _ == self.source:
            #    continue
            stabilized = True
            for v, w, weight in self.graph.edges():
                if dst_to[v] + weight < dst_to[w]:
                    dst_to[w] = dst_to[v] + weight
                    stabilized = False
                    parent[w] = v

            if stabilized:  # we can terminate early
                break

        if not stabilized:
            raise Exception("The graph contains a negative cycle")

        self._dst_to = dst_to
        self._parent = parent

    def get_distance_to(self, target):
        """
        Return shortest distance from the source to the target
        If target is not found or there is no path between source
        and the target, we'll return float('inf')
        """
        return self._dst_to.get(target, float("inf"))

    def get_path_to(self, target):
        if target not in self._parent:
            return []

        out = deque()
        t = target
        while t is not None and t in self._parent:
            out.appendleft(t)
            t = self._parent[t]

        return list(out)
