from cspatterns.datastructures import graphs

def test_undirected():
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

def test_weighted_undirected():
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

