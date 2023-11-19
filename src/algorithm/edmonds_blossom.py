
from collections import deque

from src.data_structures.blossom import Blossom
from src.data_structures.union_find import UnionFind
from src.animation.constants import BARRIER_COLOR


class EdmondsBlossom():

    def __init__(self, g):
        self.g = g
        self.expansion_list = []
        self.expansion_set = set()
        self.dsu = UnionFind(g.vertices)
        self.step = "begin"
        self.blossom = None
        self.augmenting = None
        self.barrier = None

    def run(self):
        self.run_algorithm()
        self.g.print_matching()

    def animate(self, manual_mode, speed):
        self.g.animation.animate(self.update_state, manual_mode, speed)

    def test(self):
        self.run_algorithm()
        return self.step != "fail"

    def run_algorithm(self):
        while self.update_state(None, None):
            pass

    def verify(self):
        deficiency = 0
        self.barrier = set()
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

        self.g.color_vertices(self.barrier, BARRIER_COLOR)

        return True

    def count_size(self, v):
        # counts the size of the component that containt `v` in the graph
        # G - barrier
        v.visited = True
        size = 1
        for e in v.adjacency:
            u = e.to
            if not u.visited and u not in self.barrier:
                size += self.count_size(u)
        return size

    def update_state(self, widget, event):
        if self.step == "end":
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
                        self.g.update_animation_state()
                        return True
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
            self.g.update_animation_state()
            return True

        if self.step == "expand" or self.step == "last expand":
            if len(self.expansion_list) > 0:
                self.expand_one()
            if len(self.expansion_list) == 0:
                self.expansion_clear()
                if self.step == "expand":
                    self.step = "begin"
                else:
                    self.step = "end"

        self.g.update_animation_state()
        return True

    def build_queue(self):
        self.q = deque()
        added = set()

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

    def iterate(self):
        while len(self.q) > 0:
            v = self.q.popleft()
            x = self.dsu.find(v)
            if v != x:
                # se o vértice foi contraido por outro,
                # já não é válido no novo grafo
                continue
            v = x
            for e in v.adjacency:
                u = self.dsu.find(e.to)
                if u.color == 0:
                    if u.root != v.root:
                        # caminho aumentante achado
                        self.augmenting = [u, v, e]
                        return "augment"
                    else:
                        # contrai a floração
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

    def augment(self):
        u, v, e = self.augmenting
        self.switch_match(e)
        self.alternate(u)
        self.alternate(v)

    def augmenting_path(self):
        u, v, e = self.augmenting
        edges_u = self.path_to_root(u)
        edges_v = self.path_to_root(v)
        return edges_u[::-1] + [e] + edges_v

    def path_to_root(self, v):
        edges = []
        while v.parent is not None:
            v = self.go_up(v, edges, None)
        return edges

    def fill_expansion(self):
        # adiciona todas as florações na lista de expansão
        for v in self.g.vertices:
            x = self.dsu.find(v)
            if isinstance(x, Blossom):
                self.expansion_push([x, None])

    def expand_one(self):
        [blossom, expose] = self.expansion_list.pop()
        blossom.expand(
            self.g, self.dsu, self.g.animation, expose, self.expansion_push
        )

    def add_child(self, v, u, e):
        u.root = v.root
        u.parent = e.twin
        u.color = 1 - v.color
        u.depth = v.depth + 1

    def switch_match(self, e):
        self.g.switch(e)
        if e.matched:
            # se a aresta entrou no emparelhamento, devemos ajeitar os
            # extremos dela se eles forem florações
            f = e
            for _ in range(2):
                v = self.dsu.find(f.to)
                if isinstance(v, Blossom):
                    self.expansion_push([v, f.to])
                f = e.twin

    def expansion_push(self, item):
        if item[0] in self.expansion_set:
            return
        self.expansion_list.append(item)
        self.expansion_set.add(item[0])

    def expansion_clear(self):
        self.expansion_set = set()

    def alternate(self, v):
        if v.parent is None:
            return
        self.switch_match(v.parent)
        self.alternate(self.dsu.find(v.parent.to))

    def go_up(self, u, edges, path):
        if path is not None:
            path.append(u)
        if edges is not None:
            edges.append(u.parent)
        return self.dsu.find(u.parent.to)

    def find_cycle(self, u, v, u_to_v):
        path_u = []
        path_v = []
        edges_u = []
        edges_v = []
        while u != v:
            if u.depth > v.depth:
                u = self.go_up(u, edges_u, path_u)
            else:
                v = self.go_up(v, edges_v, path_v)
        cycle = [u] + path_u[::-1] + path_v
        edge_cycle = [e.twin for e in edges_u][::-1] + [u_to_v] + edges_v
        return cycle, edge_cycle
