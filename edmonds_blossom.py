from common.graph import Graph
from collections import deque

n, m = [int(x) for x in input().split()]

g = Graph(n)

for _ in range(m):
    u, v = [int(x) for x in input().split()]
    g.add_edge(u, v)


def add_child(v, u, e):
    root[u] = root[v]
    parent[u] = e.twin
    color[u] = 1 - color[v]

def alternate(v):
    while v != root[v]:
        if color[v] == 0
            parent[v].unmatch()
        else
            parent[v].match()
        v = parent[v].to

done = False

while not done:

    done = True
    q = deque()

    color = [-1] * n
    parent = [None] * n
    root = [v for v in range(n)]
    for v in range(n):
        if not g[v].covered():
            # adiciono os vértices não emparelhados na fila
            done = False
            color[v] = 0
            q.append(g[v])
    
    while len(q) > 0:
        v = q.popleft()

        augmenting_path = False

        for e in v.adjacency:
            u = e.to
            if color[u] == 0:
                if root[u] != root[v]:
                    # caminho aumentante achado
                    e.match()
                    alternate(u)
                    alternate(v)
                    augmenting_path = True
                    break
                else:
                    # contrai a floração
            else if color[u] == -1:
                # extende a árvore alternante
                add_child(v, u, e)
                matched_e = u.get_match()
                add_child(u, matched_e.to, matched_e)
                q.append(matched_e.to)

        if augmenting_path == True:
            break
