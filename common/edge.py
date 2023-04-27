class Edge:
    """Uma aresta de um grafo. Ela é implementada como dois arcos.
       É possível acessar o outro arco com o atributo `twin`"""

    def __init__(self, u):
        self.to = u
        self.twin = None
        self.matched = False

    def __getitem__(self, i):
        return self.endpoints[i]

    def match(self):
        self.matched = True
        self.twin.matched = True

    def unmatch(self):
        self.matched = False
        self.twin.matched = False
