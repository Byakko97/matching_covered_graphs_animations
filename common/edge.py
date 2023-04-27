class Edge:
    """Uma aresta de um grafo"""

    def __init__(self, u, v):
        self.endpoints = [u, v]
        self.matched = False

    def __getitem__(self, i):
        return self.endpoints[i]

    def match(self):
        self.matched = True

    def unmatch(self):
        self.matched = False

    def neighbor(self, v):
        """devolve o extremo da aresta distinto de v"""

        return self[0] ^ self[1] ^ v
