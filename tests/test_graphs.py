from cspatterns.datastructures import graphs
from collections import deque
from itertools import combinations, combinations_with_replacement
import random

random.seed('alhambra')

def generate_graph(V, E, cls=graphs.DirectedGraph):
    edges = set()
    while len(edges) < E:
        v, w = random.randint(0, V), random.randint(0, V)
        edges.add((v,w))
    g = cls(*list(edges))
    return g

def test_postorder():
    g = generate_graph(10000, 5000)
    a = graphs.postorder_dfs(g) # 50K edges produces max recursion error
    b = graphs.postorder_iter(g)
    assert a == b

def test_directed():
    dg = graphs.DirectedGraph((0,1), (1,2), (2,3))
    assert dg.topological_sort() == [3, 2, 1, 0]
    assert graphs.postorder_iter(dg) == [3, 2, 1, 0]

    dg = graphs.DirectedGraph((0,1), (1,2), (2,3), (3,1))
    assert sorted(dg.edges()) == [(0,1), (1,2), (2,3), (3,1)]
    assert sorted(dg.reverse().edges()) == [(1, 0), (1, 3), (2, 1), (3, 2)]

    dg.add(3,4)
    dg.add(4,5)

    dg.add(5,6)
    dg.add(6,7)
    dg.add(7,5)

    print('reverse', dg.reverse().topological_sort())
    dg.add(7,0)

    assert dg.topological_sort() == [7, 6, 5, 4, 3, 2, 1, 0]
    #  assert dg.find_connected_components() == [[2, 3, 4, 5, 6, 7, 0, 1]]
    #assert dg.find_connected_components() == [deque([deque([deque([1, 2, 3]), 4, deque([5, 6, 7]), 0])])]

    # add non-cycle component
    dg.add(10, 11)
    dg.add(11, 12)
    
    assert dg.topological_sort() == [7, 6, 5, 4, 3, 2, 1, 0, 12, 11, 10]
    assert dg.find_connected_components() == [10, 11, 12, [7, 0, 1, 2, 3, 4, 5, 6]]
    #assert dg.find_connected_components() == [deque([deque([deque([1, 2, 3]), 4, deque([5, 6, 7]), 0]), 10])]
    

    # break the cycle in the first cc
    dg.delete(7, 0)
    print(list(dg.edges()))
    assert dg.topological_sort() == [7, 6, 5, 4, 3, 2, 1, 0, 12, 11, 10]
    print(dg.topological_sort())
    #assert dg.find_connected_components() == deque([10, 11, 12, 0, deque([1, 2, 3]), 4, deque([5, 6, 7])])
    assert dg.find_connected_components() == [10, 11, 12, 0, [3, 1, 2], 4, [7, 5, 6]]

    dg.add(7, 10)
    assert dg.find_connected_components() == [0, [3, 1, 2], 4, [7, 5, 6], 10, 11, 12]


def test_undirected():
    ug = graphs.UndirectedGraph((5, 6), (5, 7), (6, 7))
    assert sorted(ug.edges()) == [(5, 6), (5, 7), (6, 7)]

    ug = graphs.UndirectedGraph()
    ug.add(1,2)
    ug.add(1,2)
    ug.add(3,4)
    ug.add(1,3)

    assert ug.num_vertices() == 4
    assert ug.num_edges() == 3

    assert sorted(list(ug.adj(1))) == [2,3]
    assert sorted(list(ug.vertices())) == [1, 2, 3, 4]
    assert sorted(list(ug.edges())) == [(1,2), (1,3), (3,4)]

    ug.delete(1, 3)
    assert ug.num_vertices() == 4
    assert ug.num_edges() == 2

    ug.add(5,6)
    ug.add(6,7)
    ug.add(5,7)

    assert ug.find_connected_components() == [[(1, 2)], [(3, 4)], [(5, 6), (5, 7), (6, 7)]]



def test_weighted_undirected():
    ug = graphs.WeightedUndirectedGraph((5, 6, 1.0), (5, 7, 3.0), (6, 7, 2.0))
    assert sorted(ug.edges()) == [(5, 6, 1.0), (5, 7, 3.0), (6, 7, 2.0)]

    ug = graphs.WeightedUndirectedGraph()
    ug.add(1,2,1.0)
    ug.add(1,2,2.0)
    ug.add(3,4,3.0)
    ug.add(1,3,4.0)

    assert ug.num_vertices() == 4
    assert ug.num_edges() == 3

    assert sorted(list(ug.adj(1))) == [(2,2.0),(3,4.0)]
    assert sorted(list(ug.vertices())) == [1, 2, 3, 4]
    assert sorted(list(ug.edges())) == [(1,2,2.0), (1,3,4.0), (3,4,3.0)]

    assert ug.total_weight() == 9.0
    ug.add(1,2,0.0)
    assert ug.total_weight() == 7.0

    ug.delete(1, 3)
    assert ug.num_vertices() == 4
    assert ug.num_edges() == 2
    assert ug.total_weight() == 3.0

    ug.add(5,6,1.0)
    ug.add(6,7,2.0)
    ug.add(5,7,3.0)

    assert ug.find_connected_components() == [[(1, 2, 0.0)], [(3, 4, 3.0)], [(5, 6, 1.0), (5, 7, 3.0), (6, 7, 2.0)]]
    

if __name__ == '__main__':
    test_directed()