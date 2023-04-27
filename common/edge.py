class Edge:
    "Uma aresta de um grafo"

    def __init__(self, u, v):
        self.endpoints = [u, v]
        self.matched = False

    def match(self):
        self.matched = True

    def unmatch(self):
        self.matched = False
