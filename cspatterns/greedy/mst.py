from cspatterns.datastructures import graphs, unionfind
import heapq

class KruskalMST(object):
    """
    Find MST by growing it from the edges
    O(E logE)

    We are using UnionFind to identify connected
    components
    """
    def __init__(self, graph: graphs.WeightedUndirectedGraph):
        self.graph = graph
        self.mst = None

    def extract(self) -> graphs.WeightedUndirectedGraph:

        pq = []
        for v,w,weight in self.graph.edges():
            pq.append((weight, v, w))
        heapq.heapify(pq)

        union = unionfind.UnionFind()
        mst = graphs.WeightedUndirectedGraph()

        while pq:
            weight, v, w = heapq.heappop(pq)
            if not union.is_connected(v, w):
                union.join(v, w)
                mst.add(v, w, weight)

        return mst




class PrimMST(object):
    """
    Find MST using arbitrary vertex as a starting point
    and proceed taking the smallest edge not yet visited.
    Specialty of this impl is that instead of edges we are
    working with vertices. After the first vertex is 
    examined, it is marked as visited - not to be seen again
    
    Time: O(ElogE) - E dominates with setting/getting minimum
    Space: E
    """
    def __init__(self, graph: graphs.WeightedUndirectedGraph) -> None:
        self.graph = graph
        self.mst = None
        
    def extract(self) -> graphs.WeightedUndirectedGraph:
        if self.mst:
            return self.mst
        
        heap = []
        mst = graphs.WeightedUndirectedGraph()
        g = self.graph
        seen = set()

        # we can start from any arbitrary vertex
        v = list(self.graph.vertices())[0]
        for w,weight in g.adj(v):
            heapq.heappush(heap, (weight, v, w))
        seen.add(v)

        # keep growing the tree using the smallest vertices first
        while len(heap):
            edge_weight, v, w = heapq.heappop(heap)
            if w not in seen:
                mst.add(v,w,edge_weight)

                for ww,weight in g.adj(w):
                    if ww not in seen:
                        heapq.heappush(heap, (weight, w, ww))
                seen.add(w)

        self.mst = mst
        return self.mst



def test():
    uwg = graphs.WeightedUndirectedGraph()
    uwg.add('a', 'b', 3.0)
    uwg.add('a', 'c', 4.0)
    uwg.add('b', 'c', 3.0)
    uwg.add('c', 'd', 2.0)

    prim = PrimMST(uwg)
    mst = prim.extract()

    assert sorted(list(mst.edges())) == [('a', 'b', 3.0), ('b', 'c', 3.0), ('c', 'd', 2.0)]
    assert mst.total_weight() == 8.0

    kruskal = KruskalMST(uwg)
    mst = prim.extract()

    assert sorted(list(mst.edges())) == [('a', 'b', 3.0), ('b', 'c', 3.0), ('c', 'd', 2.0)]
    assert mst.total_weight() == 8.0