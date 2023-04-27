class Vertex:
    """Um vértice de um grafo"""

    def __init__(self):
        self.adjacency = []

    def add_neighbor(self, edge):
        self.adjacency.append(edge)

    def covered(self):
        return any([edge.matched for edge in self.adjacency])

    def get_pair(self):
        e = [edge.matched for edge in self.adjacency]
        return e[0].neighbor(self)