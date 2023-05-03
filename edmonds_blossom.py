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
    """Uma floração"""

    def __init__(self, dsu, cycle):
        super().__init__(self)
        self.cycle = cycle
        # constrói a adjacência
        for w in cycle:
            for e in w.adjacency:
                u = dsu.find(e.to)
                if u not in cycle:
                    self.add_neighbor(e)
        # contrai a floração
        dsu.add(blossom)
        for w in cycle:
            dsu.union(blossom, w)

    def expand(self, dsu, expose=None):
        # expande a floração deixando o vértice `expose` sem
        # arestas emparelahdas no ciclo
        for v in self.cycle:
            dsu.detach(v)
        if expose != None:
            alternate_list = []
            #TODO: alternar o emparelhamento deixando `expose` exposto
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

def alternate(v):
    #TODO: adiciona florações na fila de expansão
    while v != v.root:
        v.parent.switch()
        v = v.parent.to

def find_cycle(u, v):
    #TODO: acha as arestas do ciclo
    path_u = []
    path_v = []
    while u.depth > v.depth:
        path_u.append(u)
        u = u.parent.to
    while v.depth > u.depth:
        path_v.append(v)
        v = v.parent.to
    while u != v:
        path_u.append(u)
        path_v.append(v)
        u = u.parent.to
        v = v.parent.to
    cycle = [u] + path_u + path_v[::-1]
    return cycle

done = False

while not done:

    done = True
    q = deque()
    dsu = UnionFind(g.vertices)

    for v in range(n):
        g[v].color = -1
        g[v].parent = None
        g[v].root = g[v]
        g[v].depth = 0
        if not g[v].matched():
            # adiciono os vértices não emparelhados na fila
            done = False
            g[v].color = 0
            q.append(g[v])
    
    while len(q) > 0:
        v = q.popleft()

        augmenting_path = False

        for e in v.adjacency:
            u = e.to
            if u.color == 0:
                if u.root != v.root:
                    # caminho aumentante achado
                    e.switch()
                    alternate(u)
                    alternate(v)
                    augmenting_path = True
                    break
                else:
                    # contrai a floração
                    cycle = find_cycle(u, v)
                    blossom = Blossom(dsu, cycle)
            elif u.color == -1:
                # extende a árvore alternante
                add_child(v, u, e)
                matched_e = u.get_match()
                add_child(u, matched_e.to, matched_e)
                q.append(matched_e.to)

        if augmenting_path == True:
            # expande as florações por onde passou o caminho aumentante
            break

    # expande todas as florações
