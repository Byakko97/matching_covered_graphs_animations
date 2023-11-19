from __future__ import annotations

from typing import Optional, List, TYPE_CHECKING

if TYPE_CHECKING:
    from src.data_structures.edge import Edge


class Vertex:
    """Um vértice de um grafo"""

    def __init__(self, id: Optional[int] = None):
        self.id = id
        self.adjacency: List[Edge] = []
        self.color = -1
        self.parent: Optional[Edge] = None
        self.root: Vertex = self
        self.depth = 0
        self.visited = False

    def add_neighbor(self, edge: Edge) -> None:
        self.adjacency.append(edge)

    def matched(self) -> bool:
        return any([edge.matched for edge in self.adjacency])

    def get_match(self) -> Edge:
        """Devolve a aresta emparelhada incidente no vértice"""
        e = filter(lambda edge: edge.matched, self.adjacency)
        return list(e)[0]

    def reset(self) -> None:
        self.color = -1
        self.parent = None
        self.root = self
        self.depth = 0

    def print(self) -> None:
        print(self.id)
