class Vertex:
    "Um vértice de um grafo"

    def __init__(self):
        self.adjacency = []

    def add_neighbor(self, edge):
        self.adjacency.append(edge)

    def covered(self):
        return any([edge.matched for edge in self.adjacency])