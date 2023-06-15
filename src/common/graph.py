from src.common.vertex import Vertex
from src.common.edge import Edge
from src.common.graph_animation import GraphAnimation

class Graph:
    """Um grafo"""

    def __init__(self, n=0, read=False, animate=False):
        self.size = n
        m = 0
        if read:
            self.size, m = [int(x) for x in input().split()]

        self.vertices = [Vertex(i) for i in range(self.size)]

        self.animation = None if not animate else GraphAnimation(self.size)

        for _ in range(m):
            u, v = [int(x) for x in input().split()]
            self.add_edge(u, v)

    def __getitem__(self, i):
        return self.vertices[i]

    def add_edge(self, u, v):
        to_u = Edge(self.vertices[u])
        to_v = Edge(self.vertices[v])
        to_u.twin = to_v
        to_v.twin = to_u
        
        self.vertices[u].add_neighbor(to_v)
        self.vertices[v].add_neighbor(to_u)

        if self.animation != None:
            self.animation.add_edge(u, v)

    def switch(self, e):
        e.switch()
        
        if self.animation != None:
            self.animation.switch(e)   

    def print_matching(self):
        for v in self.vertices:
            for e in v.adjacency:
                if e.matched and e.to.id > v.id:
                    print(v.id, e.to.id)

    def animate(self, last=False):
        if self.animation != None:
            self.animation.animate(last)