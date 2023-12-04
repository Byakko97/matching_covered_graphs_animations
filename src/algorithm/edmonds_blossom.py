
from collections import deque
from typing import Optional, List, Tuple, Deque

from src.algorithm.algorithm_base import AlgorithmBase
from src.animation.vertex_style import BarrierStyle
from src.data_structures.blossom import Blossom
from src.data_structures.edge import Edge
from src.data_structures.graph import Graph
from src.data_structures.vertex import Vertex
from src.data_structures.union_find import UnionFind


class EdmondsBlossom(AlgorithmBase):
    def __init__(self, g: Graph):
        super().__init__(g)
        self.expansion_list: List[Tuple[Blossom, Vertex]] = []
        self.expansion_set: set[Blossom] = set()
        self.dsu = UnionFind(g.vertices)
        self.step = "begin"
        self.blossom: Optional[Blossom] = None
        self.augmenting: Tuple[Vertex, Vertex, Edge] = None
        self.barrier: set[Vertex] = set()

    def run(self) -> None:
        super().run()
        self.g.print_matching()

    def test(self) -> bool:
        super().test()
        return self.step != "fail"

    def verify(self) -> bool:
        deficiency = 0
        for v in self.g.vertices:
            count_match = [e.matched for e in v.adjacency].count(True)
            if count_match > 1:
                print("The set of edges")
                self.g.print_matching()
                print("is not a matching since " + str(v.id) +
                      " has more than one incident edge of that set.")
                return False
            deficiency += count_match == 0
            if v.color == 1 and not isinstance(self.dsu.find(v), Blossom):
                self.barrier.add(v)

        odd = 0
        for v in self.g.vertices:
            if not v.visited and v not in self.barrier:
                odd += self.count_size(v) & 1

        if deficiency != odd - len(self.barrier):
            return False

        self.g.set_vertices_style(self.barrier, BarrierStyle())

        return True

    def count_size(self, v: Vertex) -> int:
        # counts the size of the component that containt `v` in the graph
        # G - barrier
        v.visited = True
        size = 1
        for e in v.adjacency:
            u = e.to
            if not u.visited and u not in self.barrier:
                size += self.count_size(u)
        return size

    def update_state(self, widget, event) -> bool:
        if self.step == "end":
            super().update_state(widget, event)
            return False

        if self.step == "begin":
            self.build_queue()
            self.step = "search"

        if self.step == "search":
            self.step = self.iterate()
            if self.step == "shrink":
                self.g.color_alternating(self.path_to_root(self.blossom.tip()))
            else:
                if self.step == "augment":
                    self.g.color_alternating(self.augmenting_path())
                else:
                    if not self.verify():
                        self.step = "fail"
                        return False
                    self.fill_expansion()
                    if len(self.expansion_list) > 0:
                        self.step = "last expand"
                    else:
                        self.step = "end"
                    if len(self.barrier) > 0:
                        return super().update_state(widget, event)
        elif self.step == "shrink":
            self.g.color_alternating(
                self.path_to_root(self.blossom.tip()),
                undo=True,
            )
            self.blossom.shrink_animation(self.g.animation)
            self.step = "search"
        elif self.step == "augment":
            self.augment()
            if len(self.expansion_list) > 0:
                self.step = "expand"
            else:
                self.step = "begin"
            return super().update_state(widget, event)

        if self.step == "expand" or self.step == "last expand":
            if len(self.expansion_list) > 0:
                self.expand_one()
            if len(self.expansion_list) == 0:
                self.expansion_clear()
                if self.step == "expand":
                    self.step = "begin"
                else:
                    self.step = "end"

        return super().update_state(widget, event)

    def build_queue(self) -> None:
        self.q: Deque[Vertex] = deque()
        added: set[Vertex] = set()

        for v in self.g.vertices:
            vertex = self.dsu.find(v)

            if vertex in added:
                continue

            vertex.reset()
            if not vertex.matched():
                # adiciono os vértices não emparelhados na fila
                vertex.color = 0
                self.q.append(vertex)
                added.add(vertex)

    def iterate(self) -> None:
        while len(self.q) > 0:
            v = self.q.popleft()
            x = self.dsu.find(v)
            if v != x:
                # se o vértice foi contraido por outro,
                # já não é válido no novo grafo
                continue
            for e in v.adjacency:
                u = self.dsu.find(e.to)
                if u.color == 0:
                    if u.root != v.root:
                        # caminho aumentante achado
                        self.augmenting = (u, v, e)
                        return "augment"
                    else:
                        # contrai a corola
                        cycle, edge_cycle = self.find_cycle(u, v, e.twin)
                        self.blossom = Blossom(
                            self.dsu, cycle, edge_cycle, self.g.animation
                        )
                        self.q.append(self.blossom)
                        return "shrink"
                elif u.color == -1:
                    # extende a árvore alternante
                    self.add_child(v, u, e)
                    matched_e = u.get_match()
                    self.add_child(u, matched_e.to, matched_e)
                    self.q.append(matched_e.to)
        return "stop"

    def augment(self) -> None:
        u, v, e = self.augmenting
        self.switch_match(e)
        self.alternate(u)
        self.alternate(v)

    def augmenting_path(self) -> list[Edge]:
        u, v, e = self.augmenting
        edges_u = self.path_to_root(u)
        edges_v = self.path_to_root(v)
        return edges_u[::-1] + [e] + edges_v

    def path_to_root(self, v) -> list[Edge]:
        edges = []
        while v.parent is not None:
            v = self.go_up(v, edges, None)
        return edges

    def fill_expansion(self) -> None:
        # adiciona todas as corolas na lista de expansão
        for v in self.g.vertices:
            x = self.dsu.find(v)
            if isinstance(x, Blossom):
                self.expansion_push(x, None)

    def expand_one(self) -> None:
        blossom, expose = self.expansion_list.pop()
        blossom.expand(
            self.g, self.dsu, self.g.animation, expose, self.expansion_push
        )

    def add_child(self, v: Vertex, u: Vertex, e: Edge) -> None:
        u.root = v.root
        u.parent = e.twin
        u.color = 1 - v.color
        u.depth = v.depth + 1

    def switch_match(self, e: Edge) -> None:
        self.g.switch(e)
        if e.matched:
            # se a aresta entrou no emparelhamento, devemos ajeitar os
            # extremos dela se eles forem corolas
            f = e
            for _ in range(2):
                v = self.dsu.find(f.to)
                if isinstance(v, Blossom):
                    self.expansion_push(v, f.to)
                f = e.twin

    def expansion_push(self, b: Blossom, v: Optional[Vertex]) -> None:
        if b in self.expansion_set:
            return
        self.expansion_list.append((b, v))
        self.expansion_set.add(b)

    def expansion_clear(self) -> None:
        self.expansion_set = set()

    def alternate(self, v: Vertex) -> None:
        if v.parent is None:
            return
        self.switch_match(v.parent)
        self.alternate(self.dsu.find(v.parent.to))

    def go_up(
        self, u: Vertex, edges: list[Edge], path: list[Vertex]
    ) -> Vertex:
        if path is not None:
            path.append(u)
        if edges is not None:
            edges.append(u.parent)
        return self.dsu.find(u.parent.to)

    def find_cycle(
        self, u: Vertex, v: Vertex, u_to_v: Edge
    ) -> Tuple[List[Vertex], List[Edge]]:
        path_u: List[Vertex] = []
        path_v: List[Vertex] = []
        edges_u: List[Edge] = []
        edges_v: List[Edge] = []
        while u != v:
            if u.depth > v.depth:
                u = self.go_up(u, edges_u, path_u)
            else:
                v = self.go_up(v, edges_v, path_v)
        cycle = [u] + path_u[::-1] + path_v
        edge_cycle = [e.twin for e in edges_u][::-1] + [u_to_v] + edges_v
        return cycle, edge_cycle
