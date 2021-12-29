from cspatterns.datastructures import graphs
from cspatterns.linear import dfs


def test():
    """
    Testcase from Sedgewick Algorithms in Java, 3rd ed, p. 113
    """

    ug = graphs.UndirectedGraph(
        (0, 1),
        (1, 2),
        (2, 6),
        (0, 6),
        (6, 7),  # bridge
        (7, 8),
        (7, 10),
        (8, 10),
        (0, 5),  # bridge
        (5, 3),
        (5, 4),
        (3, 4),
        (4, 9),
        (4, 11),
        (9, 11),
        (11, 12),  # bridge
    )

    bridges = dfs.IdentifyBridges(ug)
    assert sorted(bridges.get_bridges()) == sorted([(6, 7), (0, 5), (11, 12)])
