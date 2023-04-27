from .vertex import Vertex
from .edge import Edge

class Graph:
    """Um grafo"""

    def __init__(self, n):
        self.size = n
        self.vertices = [Vertex() for _ in range(n)]

    def __getitem__(self, i):
        return self.vertices[i]

    def add_edge(self, u, v):
        to_u = Edge(self.vertices[u])
        to_v = Edge(self.vertices[v])
        to_u.twin = to_v
        to_v.twin = to_u
        
        self.vertices[u].add_neighbor(to_v)
        self.vertices[v].add_neighbor(to_u)
