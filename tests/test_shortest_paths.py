from cspatterns.datastructures import graphs
from cspatterns.greedy import shortest_path


def test_dijkstra():
    wug = graphs.WeightedDirectedGraph(
        ("a", "b", 3.0),
        ("b", "c", 2.0),
        ("c", "d", 1.0),
        ("a", "c", 6.0),
        ("c", "d", 1.0),
        ("b", "d", 3.10),
    )
    d = shortest_path.DijkstraShortestPath(wug, "a")
    assert d.get_distance_to("d") == 6.0
    assert d.get_distance_to("x") == float("inf")
