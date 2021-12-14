from cspatterns.datastructures import graphs
from cspatterns.dp import shortest_path


def test_bellmann_ford():
    dg = graphs.WeightedDirectedGraph(
        ("s", "u", 2),
        ("s", "v", 4),
        ("u", "v", -1),
        ("v", "t", 4),
        ("u", "w", 2),
        ("w", "t", 2),
    )

    sp = shortest_path.BellmannFord(dg, "s")

    assert sp.get_distance_to("t") == 5
    assert sp.get_path_to("t") == ["s", "u", "v", "t"]
    assert sp.get_path_to("x") == []


def test_floyd():
    dg = graphs.WeightedDirectedGraph(
        ("s", "u", 2),
        ("s", "v", 4),
        ("u", "v", -1),
        ("v", "t", 4),
        ("u", "w", 2),
        ("w", "t", 2),
    )
    sp = shortest_path.Floyd(dg)

    assert sp.get_distance_between("s", "t") == 5
    assert sp.get_path_between("s", "t") == ["s", "u", "v", "t"]
    assert sp.get_path_between("s", "x") == []
    print(sp._parent, sp._i2vmap)
    assert sp.get_path_to("t") == ["s", "u", "v", "t"]


if __name__ == "__main__":
    test_floyd()
