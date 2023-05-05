
from common.vertex import Vertex

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
            alternate_list = []
            for i in range(len(self.cycle)):
                if self.cycle[i] == expose:
                    must_match = False
                    for j in range(len(self.cycle)):
                        pos = (i + j) % len(self.cycle)
                        edge = self.edge_cycle[pos]
                        must_expose = None
                        if edge.matched != must_match:
                            must_expose = edge.to
                            edge.switch()
                        #TODO: fix bug
                        #if isinstance(cycle[pos], Blossom):
                        #    alternate_list.append([cycle[pos], must_expose])
                        must_match ^= True
                    break
            for [v, endpoint] in alternate_list:
                v.expand(dsu, endpoint)
        else:
            for v in self.cycle:
                if isinstance(v, Blossom):
                    v.expand(dsu)

    def print(self):
        print([v.id for v in self.cycle])