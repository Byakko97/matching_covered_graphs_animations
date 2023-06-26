
from collections import deque

from src.common.blossom import Blossom
from src.common.union_find import UnionFind

class EdmondsBlossom():

    def __init__(self, g):
        self.g = g
        self.expansion_list = []
        self.dsu = UnionFind(g.vertices)

    def run(self):
        self.__run()
        self.g.print_matching()

    def verify(self):
        self.__run()

        deficiency = 0
        barrier = set()
        for v in self.g.vertices:
            count_match = [e.matched for e in v.adjacency].count(True)
            if count_match > 1:
                print("The set of edges")
                self.g.print_matching()
                print("is not a matching since " + str(v.id) + " has more than one incident edge of that set.")
                return False
            deficiency += count_match == 0
            if v.color == 1 and not isinstance(self.dsu.find(v), Blossom):
                barrier.add(v)

        odd = 0
        for v in self.g.vertices:
            if v.color != 3 and not v in barrier:
                # color 3 indicates that the vertex was already counted
                odd += self.__count_size(v, barrier) & 1

        if deficiency != odd - len(barrier):
                return False

        return True

    def __count_size(self, v, barrier):
        v.color = 3
        sz = 1
        for e in v.adjacency:
            u = e.to
            if u.color != 3 and not u in barrier:
                sz += self.__count_size(u, barrier)
        return sz

    def __run(self):
        self.g.animate()
        while self.augment():
            self.__expand_all()
            self.g.animate()
        self.g.animate(True)

    def augment(self):
        q = deque()
        
        for v in self.g.vertices:
            v.color = -1
            v.parent = None
            v.root = v
            v.depth = 0
            if not v.matched():
                # adiciono os vértices não emparelhados na fila
                done = False
                v.color = 0
                q.append(v)
        
        augmenting_path = False

        while len(q) > 0:
            v = q.popleft()
            x = self.dsu.find(v)
            if v != x:
                # se o vértice foi contraido por outro, já não é válido no novo grafo
                continue
            v = x
            for e in v.adjacency:
                u = self.dsu.find(e.to)
                if u.color == 0:
                    if u.root != v.root:
                        # caminho aumentante achado
                        self.__switch_match(e)
                        self.__alternate(u)
                        self.__alternate(v)
                        augmenting_path = True
                        break
                    else:
                        # contrai a floração
                        cycle, edge_cycle = self.__find_cycle(u, v, e.twin)
                        blossom = Blossom(self.dsu, cycle, edge_cycle)
                        q.append(blossom)
                        break
                elif u.color == -1:
                    # extende a árvore alternante
                    self.__add_child(v, u, e)
                    matched_e = u.get_match()
                    self.__add_child(u, matched_e.to, matched_e)
                    q.append(matched_e.to)

            if augmenting_path == True:
                break

        return augmenting_path

    def __expand_all(self):
        # expande as florações por onde passou o caminho aumentante
        for [blossom, expose] in self.expansion_list:
            blossom.expand(self.g, self.dsu, expose)
        self.expansion_list = []

        # expande o resto de florações
        for v in self.g.vertices:
            x = self.dsu.find(v)
            if isinstance(x, Blossom):
                x.expand(self.g, self.dsu)

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
                    self.expansion_list.append([v, f.to])
                f = e.twin

    def __alternate(self, v):
        if v.parent == None:
            return
        self.__switch_match(v.parent)
        self.__alternate(self.dsu.find(v.parent.to))

    def __go_up(self, u, edges, path):
        path.append(u)
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