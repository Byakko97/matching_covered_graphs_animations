
from src.common.vertex import Vertex

class Blossom(Vertex):
    """Uma floração comprimida"""

    def __init__(self, dsu, cycle, edge_cycle):
        super().__init__()
        self.cycle = cycle
        self.edge_cycle = edge_cycle
        self.root = self.tip().root
        self.parent = self.tip().parent
        self.color = 0
        self.depth = self.tip().depth
        # constrói a adjacência
        for w in cycle:
            for e in w.adjacency:
                u = dsu.find(e.to)
                if u not in cycle:
                    self.add_neighbor(e)
        # contrai a floração
        dsu.add(self)
        for w in cycle:
            dsu.union(self, w)

    def tip(self):
            return self.cycle[0]

    def expand(self, dsu, expose=None):
        # expande a floração deixando o vértice `expose` não emparelhado 
        for v in self.cycle:
            dsu.detach(v)
        if expose != None:
            expansion_list = []
            pivot = dsu.find(expose)
            if isinstance(pivot, Blossom):
                expansion_list.append([pivot, expose])
            for i in range(len(self.cycle)):
                if self.cycle[i] == pivot:
                    must_match = False
                    for j in range(len(self.cycle)):
                        pos = (i + j) % len(self.cycle)
                        edge = self.edge_cycle[pos]
                        change = False
                        if edge.matched != must_match:
                            change = True
                            edge.switch()
                        if edge.matched:
                            if isinstance(self.cycle[pos], Blossom):
                                expansion_list.append([self.cycle[pos], edge.twin.to if change else None])
                            nxt = (pos + 1) % len(self.cycle)
                            if isinstance(self.cycle[nxt], Blossom):
                                expansion_list.append([self.cycle[nxt], edge.to if change else None])

                        must_match ^= True
                    break
            for [v, endpoint] in expansion_list:
                v.expand(dsu, endpoint)
        else:
            for v in self.cycle:
                if isinstance(v, Blossom):
                    v.expand(dsu)

    def print(self):
        print([v.id for v in self.cycle])