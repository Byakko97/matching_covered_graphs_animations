from .vertex import Vertex
from .edge import Edge

class Graph:
    "Um grafo"

    def __init__(self, n):
        self.size = n
        self.vertices = [Vertex() for _ in range(n)]

    def add_edge(self, u, v):
        edge = Edge(self.vertices[u], self.vertices[v])
        self.vertices[u].add_neighbor(edge)
        self.vertices[v].add_neighbor(edge)
