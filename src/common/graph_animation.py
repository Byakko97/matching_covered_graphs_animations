import graph_tool.all as gt
import time

class GraphAnimation:
    """Um grafo"""

    def __init__(self, n=0):
        self.g = gt.Graph(directed = False)
        if n > 0: 
            self.g.add_vertex(n)

        self.pos = None
        self.win = None

        self.matched = self.g.new_edge_property("string")

    def add_edge(self, u, v):
        e = self.g.add_edge(self.g.vertex(u), self.g.vertex(v))
        self.matched[e] = 'black'

    def switch(self, e):
        self.matched[self.g.edge(e.to.id, e.twin.to.id)] = 'red' if e.matched else 'black'

    def animate(self, last=False):
        if self.pos == None:
            self.pos = gt.sfdp_layout(self.g)

        self.win = gt.graph_draw(self.g, self.pos, edge_color=self.matched, window=self.win, return_window=True, main=last)
        time.sleep(1.5)