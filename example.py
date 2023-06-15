from graph_tool.all import *

g = Graph(directed = False)

vertices = []

for i in range(10):
    vertices.append(g.add_vertex())

for i in range(10):
    for j in range(i + 2, 10, 2):
        g.add_edge(vertices[i], vertices[j])

graph_draw(g)

g.add_edge(vertices[0], vertices[1])
graph_draw(g)
