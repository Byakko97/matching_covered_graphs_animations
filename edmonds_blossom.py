from common.graph import Graph

n, m = [int(x) for x in input().split()]

g = Graph(n)

for _ in range(m):
    u, v = [int(x) for x in input().split()]

done = False
while not done:
    done = True
    for v in range(n):
        if not g.vertices[v].covered():
            done = False