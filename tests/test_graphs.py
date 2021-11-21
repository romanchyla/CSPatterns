from cspatterns.datastructures import graphs

def test_directed():
    dg = graphs.DirectedGraph((0,1), (1,2), (2,3), (3,1))
    assert sorted(dg.edges()) == [(0,1), (1,2), (2,3), (3,1)]
    assert sorted(dg.reverse().edges()) == [(1, 0), (1, 3), (2, 1), (3, 2)]

    dg.add(3,4)
    dg.add(4,5)
    dg.add(5,6)
    dg.add(6,4)
    dg.add(6,0)

    assert dg.topological_sort() == [6, 5, 4, 3, 2, 1, 0]

    print(dg.find_connected_components())



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
    