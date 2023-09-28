class Edge:
    """Uma aresta de um grafo. Ela é implementada como dois arcos.
       É possível acessar o outro arco com o atributo `twin`"""

    def __init__(self, u):
        self.to = u
        self.twin = None
        self.matched = False

    def endpoints(self):
        return [self.to, self.twin.to]

    def switch(self):
        """muda o estado da aresta de emparelhado a não empralehado
           e viceversa"""
        self.matched ^= True
        self.twin.matched ^= True
