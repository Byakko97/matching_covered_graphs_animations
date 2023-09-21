from src.algorithm.edmond_blossom import EdmondsBlossom
from src.common.graph import Graph


class CarvalhoCheriyan():
    def __init__(self, g):
        self.g = g
        self.connected = None
        self.not_matchable_edges = []
        self.max_matching = None

    def run(self):
        self.run_algorithm()
        if self.is_matching_covered():
            print("The graph is matching covered.")
        else:
            print("The graph is not matching covered since ", end="")
            if not self.connected:
                print("is not connected.")
            elif not self.is_matchable():
                print("is not matchable.")
            else:
                print("the following edges are not matchable:")
                for edge in self.not_matchable_edges:
                    print(edge.to.id, edge.twin.to.id)

    def run_algorithm(self):
        if not self.is_connected():
            return False

        EdmondsBlossom(self.g).run_algorithm()
        if not self.is_matchable():
            return False

        for v in self.g.vertices:
            self.iterate(v)

        return len(self.not_matchable_edges) == 0

    def is_connected(self):
        self.visit(self.g[0])
        self.connected = not any(not v.visited for v in self.g.vertices)
        return self.connected

    def visit(self, v):
        v.visited = True
        for e in v.adjacency:
            u = e.to
            if not u.visited:
                self.visit(u)

    def is_matchable(self):
        return (
            self.g.size % 2 == 0 and
            self.g.size // 2 ==
            sum(edge.matched for edge in self.g.edges)
        )

    def is_matching_covered(self):
        return (
            self.connected
            and self.is_matchable()
            and len(self.not_matchable_edges) == 0
        )

    def iterate(self, v):
        aux_graph = Graph(self.g.size)
        for edge in self.g.edges:
            if edge.to == v or edge.twin.to == v:
                continue
            aux_edge = aux_graph.add_edge(edge.to.id, edge.twin.to.id)
            if edge.matched:
                aux_graph.switch(aux_edge)

        EdmondsBlossom(aux_graph).run_algorithm()
        for e in v.adjacency:
            u = e.to
            if u.id < v.id:
                continue
            if aux_graph[u.id].color != 0:
                self.not_matchable_edges.append(e)
