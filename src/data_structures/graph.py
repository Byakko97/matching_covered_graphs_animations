from typing import List

from src.data_structures.vertex import Vertex
from src.data_structures.edge import Edge
from src.animation.graph_animation import GraphAnimation


class Graph:
    """Um grafo"""

    def __init__(self, n: int = 0, read: bool = False, animate: bool = False):
        self.size = n
        m = 0
        if read:
            self.size, m = [int(x) for x in input().split()]

        self.vertices = [Vertex(i) for i in range(self.size)]

        self.animation = None if not animate else GraphAnimation(self.size)

        self.edges: List[Edge] = []
        for _ in range(m):
            u, v = [int(x) for x in input().split()]
            self.add_edge(u, v)

    def __getitem__(self, i: int) -> Vertex:
        return self.vertices[i]

    def add_edge(self, u: int, v: int) -> None:
        to_u = Edge(self.vertices[u])
        to_v = Edge(self.vertices[v])
        to_u.twin = to_v
        to_v.twin = to_u

        self.vertices[u].add_neighbor(to_v)
        self.vertices[v].add_neighbor(to_u)

        if self.animation is not None:
            self.animation.add_edge(u, v)

        self.edges.append(to_u)
        return to_u

    def switch(self, e: Edge) -> None:
        e.switch()
        self.match_color(e)

    def match_color(self, e: Edge) -> None:
        if self.animation is not None:
            self.animation.match_color(e)

    def print_matching(self) -> None:
        for v in self.vertices:
            for e in v.adjacency:
                if e.matched and e.to.id > v.id:
                    print(v.id, e.to.id)

    def color_vertices(self, vertices: List[Vertex], color: str) -> None:
        if self.animation is not None:
            self.animation.color_vertices(vertices, color)

    def color_edges(self, edges: List[Edge], color: str) -> None:
        if self.animation is not None:
            self.animation.color_edges(edges, color)

    def color_alternating(self, path: List[Edge], undo: bool = False) -> None:
        if self.animation is not None:
            self.animation.color_alternating(path, undo)

    def update_animation_state(self) -> None:
        if self.animation is not None:
            self.animation.update_state()

    def show_labels(self) -> None:
        if self.animation is not None:
            self.animation.show_labels(self.vertices)
