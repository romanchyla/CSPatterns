from collections import defaultdict, deque


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
            if _ == self.source:
                continue
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
