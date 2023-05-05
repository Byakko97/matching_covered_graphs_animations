from .vertex import Vertex
from .edge import Edge

class Graph:
    """Um grafo"""

    def __init__(self, n=0):
        self.size = n
        self.vertices = [Vertex(i) for i in range(n)]

    def __getitem__(self, i):
        return self.vertices[i]

    def add_edge(self, u, v):
        to_u = Edge(self.vertices[u])
        to_v = Edge(self.vertices[v])
        to_u.twin = to_v
        to_v.twin = to_u
        
        self.vertices[u].add_neighbor(to_v)
        self.vertices[v].add_neighbor(to_u)

    def print_matching(self):
        for v in self.vertices:
            for e in v.adjacency:
                if e.matched and e.to.id > v.id:
                    print(v.id, e.to.id)
        print()

    def read(self):
        n, m = [int(x) for x in input().split()]
        self.__init__(n)
        for _ in range(m):
            u, v = [int(x) for x in input().split()]
            self.add_edge(u, v)