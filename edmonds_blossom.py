from common.graph import Graph
from common.vertex import Vertex
from collections import deque
from common.union_find import UnionFind

n, m = [int(x) for x in input().split()]

g = Graph(n)

for _ in range(m):
    u, v = [int(x) for x in input().split()]
    g.add_edge(u, v)


def add_child(v, u, e):
    u.root = v.root
    u.parent = e.twin
    u.color = 1 - v.color
    u.depth = v.depth + 1

def alternate(v):
    while v != v.root:
        while v != dsu.find(v):
            expand(dsu.find(v))
        v.parent.switch()
        v = v.parent.to

def find_cycle(u, v):
    cycle = []
    while u.depth > v.depth:
        cycle.append(u)
        u = u.parent.to
    while v.depth > u.depth:
        cycle.append(v)
        v = v.parent.to
    while u != v:
        cycle.append(u)
        cycle.append(v)
        u = u.parent.to
        v = v.parent.to
    cycle.append(u)
    return cycle

def shrink(cycle):
    x = Vertex()
    x.cycle = cycle
    x.root = x.tip().root
    x.parent = x.tip().parent
    x.color = 0
    x.depth = x.tip().depth
    dsu.add(x)
    for v in cycle:
        dsu.union(x, v)
        for e in v.adjacency:
            if not e.to in cycle:
                x.add_neighbor(e)
    return x

def expand(x):
    for v in x.cycle:
        dsu.detach(v)

dsu = UnionFind(g.vertices)

while True:

    q = deque()

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

        for e in v.adjacency:
            u = e.to
            if u.color == 0:
                if u.root != v.root:
                    # caminho aumentante achado
                    e.switch()
                    alternate(u)
                    alternate(v)
                    break
                else:
                    # contrai a floração
                    cycle = find_cycle(u, v)
                    x = shrink(cycle)
                    q.append(x)
            elif u.color == -1:
                # extende a árvore alternante
                add_child(v, u, e)
                matched_e = u.get_match()
                add_child(u, matched_e.to, matched_e)
                q.append(matched_e.to)

    if len(q) == 0:
        break

    for v in range(n):
        while dsu.find(g[v]) != g[v]:
            # ainda temos florações comprimidas
            expand(dsu.find(g[v]))
