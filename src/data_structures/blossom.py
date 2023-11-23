from __future__ import annotations
from typing import Callable, Optional, TYPE_CHECKING
from src.animation.constants import FLOWER_COLOR
from src.data_structures.edge import Edge
from src.data_structures.vertex import Vertex
from src.data_structures.union_find import UnionFind
if TYPE_CHECKING:
    from src.animation.graph_animation import GraphAnimation
    from src.data_structures.graph import Graph


class Blossom(Vertex):
    """Uma floração comprimida"""

    def __init__(
        self,
        dsu: UnionFind,
        cycle: list[Vertex],
        edge_cycle: list[Edge],
        animation: Optional[GraphAnimation]
    ):
        super().__init__()
        self.cycle = cycle
        self.edge_cycle = edge_cycle
        self.root = self.tip().root
        self.parent = self.tip().parent
        self.color = 0
        self.depth = self.tip().depth

        # constrói a adjacência
        for w in cycle:
            for e in w.adjacency:
                u = dsu.find(e.to)
                if u not in cycle:
                    self.add_neighbor(e)

        # contrai a floração
        dsu.add(self)
        for w in cycle:
            dsu.union(self, w)
            w.color = 0

        if animation is not None:
            self.old_pos = None
            animation.color_vertices(self.get_vertices(), FLOWER_COLOR)
            animation.color_alternating(self.edge_cycle)

    def shrink_animation(self, animation) -> None:
        if animation is not None:
            self.old_pos = animation.shrink(
                self.get_vertices(), self.edge_cycle,
            )

    def get_vertices(self) -> list[Vertex]:
        vertices = []
        for v in self.cycle:
            if isinstance(v, Blossom):
                vertices.extend(v.get_vertices())
            else:
                vertices.append(v)
        return vertices

    def tip(self) -> Vertex:
        return self.cycle[0]

    def expand(
        self,
        g: Graph,
        dsu: UnionFind,
        animation: Optional[GraphAnimation],
        expose: Optional[Vertex],
        push: Callable[['Blossom', Optional[Vertex]], None],
    ) -> None:
        # expande a floração deixando o vértice `expose` não emparelhado

        for v in self.cycle:
            dsu.detach(v)
        if animation is not None:
            animation.expand(self.get_vertices(), self.old_pos, dsu)

        if expose is not None:
            pivot = dsu.find(expose)
            if isinstance(pivot, Blossom):
                push(pivot, expose)
            for i in range(len(self.cycle)):
                if self.cycle[i] == pivot:
                    must_match = False
                    for j in range(len(self.cycle)):
                        pos = (i + j) % len(self.cycle)
                        edge = self.edge_cycle[pos]
                        change = False
                        if edge.matched != must_match:
                            change = True
                            g.switch(edge)
                        if edge.matched:
                            if isinstance(self.cycle[pos], Blossom):
                                push(self.cycle[pos], edge.twin.to if change
                                     else None)
                            nxt = (pos + 1) % len(self.cycle)
                            if isinstance(self.cycle[nxt], Blossom):
                                push(self.cycle[nxt], edge.to if change
                                     else None)

                        must_match ^= True
                    break
        else:
            for v in self.cycle:
                if isinstance(v, Blossom):
                    push(v, None)

    def print(self) -> None:
        print([v.id for v in self.cycle])
