from common.graph import Graph
from common.vertex import Vertex
from collections import deque
from common.union_find import UnionFind

#TODO: create read function for graphs
n, m = [int(x) for x in input().split()]

g = Graph(n)

for _ in range(m):
    u, v = [int(x) for x in input().split()]
    g.add_edge(u, v)

class Blossom(Vertex):
    """Uma floração comprimida"""

    def __init__(self, dsu, cycle, edge_cycle):
        super().__init__(self)
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

    def tip(self):
            return self.cycle[0]

    def expand(self, dsu, expose=None):
        # expande a floração deixando o vértice `expose` não emparelhado 
        for v in self.cycle:
            dsu.detach(v)
        if expose != None:
            alternate_list = []
            for i in range(len(cycle)):
                if cycle[i] == expose:
                    must_match = False
                    for j in range(len(cycle)):
                        pos = (i + j) % len(cycle)
                        edge = edge_cycle[pos]
                        must_expose = None
                        if edge.matched != must_match:
                            must_expose = edge.to
                            edge.switch()
                        if isinstance(cycle[pos], Blossom):
                            alternate_list.append([cycle[pos], must_expose])
                        must_match ^= True
                    break
            for [v, endpoint] in alternate_list:
                v.expand(dsu, endpoint)
        else:
            for v in self.cycle:
                if isinstance(v, Blossom):
                    v.expand(dsu)

def add_child(v, u, e):
    u.root = v.root
    u.parent = e.twin
    u.color = 1 - v.color
    u.depth = v.depth + 1

expansion_list = []
def alternate(v, e):
    if isinstance(v, Blossom):
        expansion_list.append([v, e])
    if v.parent == None:
        return
    v.parent.switch()
    alternate(dsu.find(v.parent.to), v.parent)

def find_cycle(u, v, u_to_v):
    path_u = []
    path_v = []
    edges_u = []
    edges_v = []
    while u.depth > v.depth:
        path_u.append(u)
        edges_u.append(u.parent)
        u = u.parent.to
    while v.depth > u.depth:
        path_v.append(v)
        edges_v.append(v.parent)
        v = v.parent.to
    while u != v:
        path_u.append(u)
        edges_u.append(u.parent)
        path_v.append(v)
        edges_v.append(v.parent)
        u = u.parent.to
        v = v.parent.to
    cycle = [u] + path_u[::-1] + path_v
    edge_cycle = [e.twin for e in edges_u] + u_to_v + edges_v
    return cycle, edge_cycle

dsu = UnionFind(g.vertices)

while True:

    q = deque()

    for v in g.vertices:
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
        for e in v.adjacency:
            u = e.to
            if u.color == 0:
                if u.root != v.root:
                    # caminho aumentante achado
                    e.switch()
                    alternate(u, e)
                    alternate(v, e.twin)
                    augmenting_path = True
                    break
                else:
                    # contrai a floração
                    cycle, edge_cycle = find_cycle(u, v, e.twin)
                    blossom = Blossom(dsu, cycle, edge_cycle)
            elif u.color == -1:
                # extende a árvore alternante
                add_child(v, u, e)
                matched_e = u.get_match()
                add_child(u, matched_e.to, matched_e)
                q.append(matched_e.to)

        if augmenting_path == True:
            # expande as florações por onde passou o caminho aumentante
            for [blossom, edge] in expansion_list:
                blossom.expand(dsu, edge.to)
            break

    # expande todas as florações
    for v in g.vertices:
        x = dsu.find(v)
        if isinstance(x, Blossom):
            x.expand(dsu)

    if augmenting_path == False:
        # emparelhamento máximo achado
        break