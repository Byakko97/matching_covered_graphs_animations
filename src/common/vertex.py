class Vertex:
    """Um vértice de um grafo"""

    def __init__(self, id=None):
        self.id = id
        self.adjacency = []
        self.color = -1
        self.parent = None
        self.root = self
        self.depth = 0

    def add_neighbor(self, edge):
        self.adjacency.append(edge)

    def matched(self):
        return any([edge.matched for edge in self.adjacency])

    def get_match(self):
        """Devolve a aresta emparelhada incidente no vértice"""
        e = filter(lambda edge: edge.matched, self.adjacency)
        return list(e)[0]

    def print(self):
        print(self.id)
