
from collections import deque

from common.blossom import Blossom
from common.graph import Graph
from common.union_find import UnionFind

g = Graph()
g.read()

def add_child(v, u, e):
    u.root = v.root
    u.parent = e.twin
    u.color = 1 - v.color
    u.depth = v.depth + 1

expansion_list = []
def switch_match(e):
    e.switch()
    if e.matched:
        # se a aresta entrou no emparelhamento, devemos ajeitar os
        # extremos dela se eles forem florações
        f = e
        for _ in range(2):
            v = dsu.find(f.to)
            if isinstance(v, Blossom):
                expansion_list.append([v, f.to])
            f = e.twin
def alternate(v):
    if v.parent == None:
        return
    switch_match(v.parent)
    alternate(dsu.find(v.parent.to))

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
    edge_cycle = [e.twin for e in edges_u][::-1] + [u_to_v] + edges_v
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
        x = dsu.find(v)
        if v != x:
            # se o vértice foi contraido por outro, já não é válido no novo grafo
            continue
        v = x
        for e in v.adjacency:
            u = dsu.find(e.to)
            if u.color == 0:
                if u.root != v.root:
                    # caminho aumentante achado
                    switch_match(e)
                    alternate(u)
                    alternate(v)
                    augmenting_path = True
                    break
                else:
                    # contrai a floração
                    cycle, edge_cycle = find_cycle(u, v, e.twin)
                    blossom = Blossom(dsu, cycle, edge_cycle)
                    q.append(blossom)
                    break
            elif u.color == -1:
                # extende a árvore alternante
                add_child(v, u, e)
                matched_e = u.get_match()
                add_child(u, matched_e.to, matched_e)
                q.append(matched_e.to)

        if augmenting_path == True:
            # expande as florações por onde passou o caminho aumentante
            for [blossom, expose] in expansion_list:
                blossom.expand(dsu, expose)
            break

    # expande todas as florações
    for v in g.vertices:
        x = dsu.find(v)
        if isinstance(x, Blossom):
            x.expand(dsu)

    if augmenting_path == False:
        # emparelhamento máximo achado
        break

g.print_matching()