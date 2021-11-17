from cspatterns.datastructures import unionfind


def test_unionfind():
    uf = unionfind.UnionFind('abcdef')

    assert uf.num_components() == 6
    assert uf.size() == 6

    uf.join('a', 'b')
    uf.join('c', 'd')
    uf.join('e', 'f')

    assert uf.num_components() == 3
    assert uf.size() == 6

    assert uf.is_connected('a', 'b') == True
    assert uf.is_connected('a', 'f') == False

    uf.join('f', 'a')
    assert uf.num_components() == 2

    uf.join('f', 'd')
    assert uf.num_components() == 1
    assert uf.is_connected('a', 'c') == True


    # should be no-op
    uf.join('f', 'c')
    assert uf.num_components() == 1