import types

from cspatterns.datastructures import graphs


class IdentifyBridges(object):
    """
    Bridges inside graph are edges, which when deleted, would sever
    a connection of a group of vertices (subgraph) to other parts
    of the graph. They are identified easily - though smartly - because
    when we do DFS of the graph, and keep building information about
    the (tree) traversal, we can differentiate:

    - backlinks (tracking the lowest reachable pre-order num of any
        subcomponent; if it is not pointing to a parent, then we
        know we have discovered a bridge)


    If a vertex has no incoming link (looping back to it from any of its
    children), then that vertex/edge serves as a bridge to that
    isolated island of edges

    The crucial piece of info is:

    ord[v] > ord[w] = downlink
    ord[v] < ord[w] = backlink (if v is not a parent)

    """

    def __init__(self, graph):
        """
        :param: graph - instance of the graph; the graph must not change
            during calculation; if you cannot guarantee that, pass in
            a copy/clone of the graph
        """
        self._graph = graph

        # helper func to deal with un/weighted .adj()
        if isinstance(graph, graphs.UndirectedGraph):

            def get_adj(self, v):
                for w in self._graph.adj(v):
                    yield (w, 0.0)

        else:

            def get_adj(self, v):
                for w, weight in self._adj(v):
                    yield (w, weight)

        setattr(self, "_adj", types.MethodType(get_adj, self))
        self._run_search()

    def get_bridges(self):
        return self._bridges

    def _run_search(self):

        bridges = []

        # our vertices can be non-ints, so we need mapping
        # the iteration over the dictionary is guaranteed stable in python; so we could actually avoid using the vmap
        # if I do a 2nd pass and map the vid -> vertex key; # the values must not change however
        # https://stackoverflow.com/questions/2053021/is-the-order-of-a-python-dictionary-guaranteed-over-iterations

        vmap = {}
        ccount = 0
        ord = [-1] * self._graph.num_vertices()
        low = [-1] * self._graph.num_vertices()

        def dfs(v, parent):
            nonlocal ccount
            vmap[v] = ccount
            vid = ccount
            ord[vid] = ccount
            low[vid] = ccount
            ccount += 1

            parentid = ord[vmap[parent]]

            for w, _ in self._adj(v):
                if w not in vmap:
                    dfs(w, v)
                    wid = vmap[w]
                    if low[wid] < low[vid]:  # backlink, pointing to some of our ancestor
                        low[vid] = low[wid]
                elif (
                    vmap[w] != parentid
                ):  # these are downlinks - we have already explored the subgraph
                    wid = vmap[w]
                    if ord[wid] < ord[vid]:
                        low[vid] = low[wid]

            if low[vid] == ord[vid] and v != parent:
                bridges.append((parent, v))

        for v in self._graph.vertices():
            if v not in vmap:
                dfs(v, v)

        self._bridges = bridges

        # debugging output
        # print("vertex \t", "\t".join([str(x) for x in self._graph.vertices()]))
        # print("ord\t", "\t".join([str(vmap[x]) for x in self._graph.vertices()]))
        # print("low\t", "\t".join([str(low[vmap[x]]) for x in self._graph.vertices()]))
