from typing import List

from src.data_structures.vertex import Vertex
from src.data_structures.edge import Edge
from src.animation.graph_animation import GraphAnimation
from src.animation.vertex_style import VertexStyle
from src.animation.edge_style import EdgeStyle


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
        self.match_style(e)

    def match_style(self, e: Edge) -> None:
        if self.animation is not None:
            self.animation.match_style(e)

    def print_matching(self) -> None:
        for v in self.vertices:
            for e in v.adjacency:
                if e.matched and e.to.id > v.id:
                    print(v.id, e.to.id)

    def set_vertices_style(
        self, vertices: List[Vertex], style: VertexStyle,
    ) -> None:
        if self.animation is not None:
            self.animation.set_vertices_style(vertices, style)

    def set_edges_style(self, edges: List[Edge], style: EdgeStyle) -> None:
        if self.animation is not None:
            self.animation.set_edges_style(edges, style)

    def color_alternating(self, path: List[Edge], undo: bool = False) -> None:
        if self.animation is not None:
            self.animation.color_alternating(path, undo)

    def update_animation_state(self) -> None:
        if self.animation is not None:
            self.animation.update_state()
