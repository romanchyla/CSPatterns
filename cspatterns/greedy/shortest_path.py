from cspatterns.datastructures import graphs
import heapq

class DijkstraShortestPath(object):
    def __init__(self, graph, source) -> None:
        super().__init__()
        self.source = source
        self.graph = graph

        if not graph.has_vertex(source):
            raise Exception('Source vertex {} is missing from the graph'.format(source))

        self._dst_to = self._extract_shortest_distances()

    def _extract_shortest_distances(self):
        """
        Run Dijkstra's shortest path -- the edge weights should not be
        negative. We'll happily process those but you cannot expect
        results to be correct.
        """
        dst_to = {}
        pq = [(0, self.source)]
        g = self.graph

        for v in g.vertices():
            dst_to[v] = float('inf')
        dst_to[self.source] = 0

        while pq:
            curr_weight, v = heapq.heappop(pq)
            #print('v={} weight={}'.format(v, curr_weight))
            for w, edge_weight in g.adj(v):
                if dst_to[v] + edge_weight < dst_to[w]:
                    #print('dst_to[v]={}, adding w={}'.format(dst_to[v], w))
                    dst_to[w] = dst_to[v] + edge_weight
                    heapq.heappush(pq, (dst_to[w], w)) #TODO: if we had indexed PQ we can replace value for 'w'
        return dst_to

    def get_distance_to(self, target):
        """
        Return shortest distance from the source to the target
        If target is not found or there is no path between source
        and the target, we'll return float('inf')
        """
        return self._dst_to.get(target, float('inf'))
    