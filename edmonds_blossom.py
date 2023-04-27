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
        u = u.parent.to
        v = v.parent.to
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
                    cycle = find_cycle(u, v)
                    # contrai a floração
                    pass
            elif u.color == -1:
                # extende a árvore alternante
                add_child(v, u, e)
                matched_e = u.get_match()
                add_child(u, matched_e.to, matched_e)
                q.append(matched_e.to)

        if augmenting_path == True:
            break
