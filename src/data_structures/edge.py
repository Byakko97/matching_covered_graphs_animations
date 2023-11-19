from typing import Tuple

from src.data_structures.vertex import Vertex


class Edge:
    """Uma aresta de um grafo. Ela é implementada como dois arcos.
       É possível acessar o outro arco com o atributo `twin`"""

    def __init__(self, u: Vertex):
        self.to: Vertex = u
        self.twin: Edge
        self.matched = False

    def endpoints(self) -> Tuple[Vertex, Vertex]:
        return (self.to, self.twin.to)

    def switch(self) -> None:
        """muda o estado da aresta de emparelhado a não empralehado
           e viceversa"""
        self.matched ^= True
        self.twin.matched ^= True
