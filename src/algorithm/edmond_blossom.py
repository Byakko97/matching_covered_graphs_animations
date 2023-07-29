
from collections import deque

from src.common.blossom import Blossom
from src.common.union_find import UnionFind


class EdmondsBlossom():

    def __init__(self, g):
        self.g = g
        self.expansion_list = []
        self.expansion_set = set()
        self.dsu = UnionFind(g.vertices)
        self.step = "begin"
        self.blossom = None
        self.augmenting = None

    def run(self):
        self.__run()
        self.g.print_matching()

    def animate(self, manual_mode, speed):
        self.g.animation.animate(self.__update_state, manual_mode, speed)

    def test(self):
        self.__run()
        return self.verify()

    def verify(self):
        deficiency = 0
        barrier = set()
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
                barrier.add(v)

        odd = 0
        for v in self.g.vertices:
            if v.color != 3 and v not in barrier:
                # color 3 indicates that the vertex was already counted
                odd += self.__count_size(v, barrier) & 1

        if deficiency != odd - len(barrier):
            return False

        if self.g.animation is not None:
            self.g.animation.color_vertices(barrier, "cyan")

        return True

    def __count_size(self, v, barrier):
        v.color = 3
        sz = 1
        for e in v.adjacency:
            u = e.to
            if u.color != 3 and u not in barrier:
                sz += self.__count_size(u, barrier)
        return sz

    def __update_state(self, widget, event):
        if self.step == "end":
            return False

        if self.step == "begin":
            self.__build_queue()
            self.step = "search"

        if self.step == "search":
            self.step = self.__iterate()
            if self.step == "shrink":
                self.g.animation.color_alternating(
                    self.__path_to_root(self.blossom.tip())
                    )
            else:
                if self.step == "augment":
                    self.g.animation.color_alternating(
                        self.__augmenting_path()
                        )
                else:
                    assert self.verify()
                    self.__fill_expansion()
                    if len(self.expansion_list) > 0:
                        self.step = "last expand"
                    else:
                        self.step = "end"
        elif self.step == "shrink":
            self.g.animation.color_alternating(
                self.__path_to_root(self.blossom.tip()), undo=True
                )
            self.blossom.shrink_animation(self.g.animation)
            self.step = "search"
        elif self.step == "augment":
            self.__augment()
            self.__fill_expansion()
            if len(self.expansion_list) > 0:
                self.step = "expand"
            else:
                self.step = "begin"
            self.g.animation.update_state()
            return True

        if self.step == "expand" or self.step == "last expand":
            if len(self.expansion_list) > 0:
                self.__expand_one()
            if len(self.expansion_list) == 0:
                self.__expansion_clear()
                if self.step == "expand":
                    self.step = "begin"
                else:
                    self.step = "end"

        self.g.animation.update_state()
        return True

    def __run(self):
        while True:
            self.__build_queue()
            while True:  # shrink found blossoms
                result = self.__iterate()
                if result != "shrink":
                    if result == "augment":
                        self.__augment()
                    break
            if result == "stop":
                break
            self.__expand_all()

    def __build_queue(self):
        self.q = deque()

        for v in self.g.vertices:
            v.color = -1
            v.parent = None
            v.root = v
            v.depth = 0
            if not v.matched():
                # adiciono os vértices não emparelhados na fila
                v.color = 0
                self.q.append(v)

    def __iterate(self):
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
                        cycle, edge_cycle = self.__find_cycle(u, v, e.twin)
                        self.blossom = Blossom(
                            self.dsu, cycle, edge_cycle, self.g.animation
                            )
                        self.q.append(self.blossom)
                        return "shrink"
                elif u.color == -1:
                    # extende a árvore alternante
                    self.__add_child(v, u, e)
                    matched_e = u.get_match()
                    self.__add_child(u, matched_e.to, matched_e)
                    self.q.append(matched_e.to)
        return "stop"

    def __augment(self):
        u, v, e = self.augmenting
        self.__switch_match(e)
        self.__alternate(u)
        self.__alternate(v)

    def __augmenting_path(self):
        u, v, e = self.augmenting
        edges_u = self.__path_to_root(u)
        edges_v = self.__path_to_root(v)
        return edges_u[::-1] + [e] + edges_v

    def __path_to_root(self, v):
        edges = []
        while v.parent is not None:
            v = self.__go_up(v, edges, None)
        return edges

    def __expand_all(self):
        self.__fill_expansion()

        # expande as florações
        while len(self.expansion_list) > 0:
            self.__expand_one()

        self.__expansion_clear()

    def __fill_expansion(self):
        # adiciona todas as florações na lista de expansão
        for v in self.g.vertices:
            x = self.dsu.find(v)
            if isinstance(x, Blossom):
                self.__expansion_push([x, None])

    def __expand_one(self):
        [blossom, expose] = self.expansion_list.pop()
        blossom.expand(
            self.g, self.dsu, self.g.animation, expose, self.__expansion_push
            )

    def __add_child(self, v, u, e):
        u.root = v.root
        u.parent = e.twin
        u.color = 1 - v.color
        u.depth = v.depth + 1

    def __switch_match(self, e):
        self.g.switch(e)
        if e.matched:
            # se a aresta entrou no emparelhamento, devemos ajeitar os
            # extremos dela se eles forem florações
            f = e
            for _ in range(2):
                v = self.dsu.find(f.to)
                if isinstance(v, Blossom):
                    self.__expansion_push([v, f.to])
                f = e.twin

    def __expansion_push(self, item):
        if item[0] in self.expansion_set:
            return
        self.expansion_list.append(item)
        self.expansion_set.add(item[0])

    def __expansion_clear(self):
        self.expansion_set = set()

    def __alternate(self, v):
        if v.parent is None:
            return
        self.__switch_match(v.parent)
        self.__alternate(self.dsu.find(v.parent.to))

    def __go_up(self, u, edges, path):
        if path is not None:
            path.append(u)
        if edges is not None:
            edges.append(u.parent)
        return self.dsu.find(u.parent.to)

    def __find_cycle(self, u, v, u_to_v):
        path_u = []
        path_v = []
        edges_u = []
        edges_v = []
        while u.depth > v.depth:
            u = self.__go_up(u, edges_u, path_u)
        while v.depth > u.depth:
            v = self.__go_up(v, edges_v, path_v)
        while u != v:
            u = self.__go_up(u, edges_u, path_u)
            v = self.__go_up(v, edges_v, path_v)
        cycle = [u] + path_u[::-1] + path_v
        edge_cycle = [e.twin for e in edges_u][::-1] + [u_to_v] + edges_v
        return cycle, edge_cycle
