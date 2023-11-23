from typing import Optional, List

from src.algorithm.algorithm_base import AlgorithmBase
from src.algorithm.edmonds_blossom import EdmondsBlossom
from src.data_structures.graph import Graph
from src.data_structures.vertex import Vertex
from src.data_structures.edge import Edge
from src.animation.constants import (
    VERTEX_COLOR,
    DELETED_COLOR,
    NOT_MATCHABLE_COLOR,
)


class CarvalhoCheriyan(AlgorithmBase):
    def __init__(self, g: Graph):
        super().__init__(g)
        self.connected: Optional[bool] = None
        self.not_matchable_edges: List[Edge] = []

        self.step = "begin"
        self.iteration_pos = 0

    def run(self) -> None:
        super().run()
        if self.is_matching_covered():
            print("The graph is matching covered.")
        else:
            print("The graph is not matching covered since ", end="")
            if self.g.size == 0:
                print("doesn't have at least one edge")
            elif not self.connected:
                print("is not connected.")
            elif not self.is_matchable(self.g, self.g.size):
                print("is not matchable.")
            else:
                print("the following edges are not matchable:")
                for edge in self.not_matchable_edges:
                    print(edge.to.id, edge.twin.to.id)

    def test(self) -> bool:
        super().test()
        return self.verify()

    def verify(self) -> bool:
        if not self.connected:
            return True

        expected_edges: List[Edge] = []
        for edge in self.g.edges:
            u, v = edge.endpoints()
            aux_graph = Graph(self.g.size)
            for other_edge in self.g.edges:
                if (other_edge == edge
                        or u in other_edge.endpoints()
                        or v in other_edge.endpoints()):
                    continue
                aux_graph.add_edge(other_edge.to.id, other_edge.twin.to.id)

            EdmondsBlossom(aux_graph).run_algorithm()
            if not self.is_matchable(aux_graph, self.g.size - 2):
                if edge.to.id < edge.twin.to.id:
                    edge = edge.twin
                expected_edges.append(edge)

        actual_edges: List[Edge] = []
        for edge in self.not_matchable_edges:
            if edge.to.id < edge.twin.to.id:
                edge = edge.twin
            actual_edges.append(edge)
        return set(expected_edges) == set(actual_edges)

    def update_state(self, widget, event) -> bool:
        if self.step == "end":
            return False

        if self.step == "begin":
            if self.g.size == 0 or not self.is_connected():
                self.step = "end"
            else:
                edmonds = EdmondsBlossom(self.g)
                edmonds.run_algorithm()
                self.g.color_vertices(edmonds.barrier, VERTEX_COLOR)
                if not self.is_matchable(self.g, self.g.size):
                    unmatched_vertices = [
                        v for v in self.g.vertices if not v.matched()
                    ]
                    self.g.color_vertices(
                        unmatched_vertices,
                        NOT_MATCHABLE_COLOR,
                    )

                    self.not_matchable_edges = self.g.edges
                    self.step = "end"
                else:
                    self.step = "delete_vertex"
        elif self.step == "delete_vertex":
            self.delete_vertex(self.g[self.iteration_pos])
            self.step = "iterate"
        elif self.step == "iterate":
            self.iterate(self.g[self.iteration_pos])
            self.step = "undelete_vertex"
        elif self.step == "undelete_vertex":
            for v in self.g.vertices:
                v.reset()
            self.g.show_labels()
            self.undelete_vertex(self.g[self.iteration_pos])
            self.iteration_pos += 1
            if self.iteration_pos == self.g.size:
                self.step = "final"
            else:
                self.step = "delete_vertex"
        elif self.step == "final":
            self.g.color_edges(self.not_matchable_edges, NOT_MATCHABLE_COLOR)
            self.step = "end"

        return super().update_state(widget, event)

    def is_connected(self) -> bool:
        self.visit(self.g[0])
        self.connected = not any(not v.visited for v in self.g.vertices)
        for v in self.g.vertices:
            v.visited = False
        return self.connected

    def visit(self, v: Vertex) -> None:
        v.visited = True
        for e in v.adjacency:
            u = e.to
            if not u.visited:
                self.visit(u)

    def is_matchable(self, graph: Graph, size: int) -> bool:
        return (
            size % 2 == 0 and
            size // 2 ==
            sum(edge.matched for edge in graph.edges)
        )

    def is_matching_covered(self) -> bool:
        return (
            self.connected
            and self.is_matchable(self.g, self.g.size)
            and len(self.not_matchable_edges) == 0
        )

    def delete_vertex(self, v: Vertex) -> None:
        self.g.color_vertices([v], DELETED_COLOR)
        deleted_edges = []

        self.current_aux_graph = Graph(self.g.size)
        for edge in self.g.edges:
            if edge.to == v or edge.twin.to == v:
                deleted_edges.append(edge)
                continue
            aux_edge = self.current_aux_graph.add_edge(
                edge.to.id, edge.twin.to.id
            )
            if edge.matched:
                self.current_aux_graph.switch(aux_edge)

        self.g.color_edges(deleted_edges, DELETED_COLOR)

    def iterate(self, v: Vertex) -> None:
        EdmondsBlossom(self.current_aux_graph).run_algorithm()
        new_not_matchables: List[Edge] = []
        for e in v.adjacency:
            u = e.to
            if u.id < v.id:
                continue
            if self.current_aux_graph[u.id].color != 0:
                new_not_matchables.append(e)
                self.not_matchable_edges.append(e)

        for u in self.g.vertices:
            if u != v:
                u.color = self.current_aux_graph[u.id].color
        self.g.show_labels()
        self.g.color_edges(new_not_matchables, NOT_MATCHABLE_COLOR)

    def undelete_vertex(self, v: Vertex) -> None:
        self.g.color_vertices([v], VERTEX_COLOR)
        for e in v.adjacency:
            self.g.match_color(e)
