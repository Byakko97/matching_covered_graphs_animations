import graph_tool.all as gt
import copy

from gi.repository import Gtk

from src.common.blossom import Blossom

class GraphAnimation:
    """Animação de um grafo"""

    def __init__(self, n=0):
        self.g = gt.Graph(directed = False)
        if n > 0: 
            self.g.add_vertex(n)

        self.pos = None
        self.win = None

        self.matched_color = self.g.new_edge_property("string")
        self.matched_width = self.g.new_edge_property("float")
        self.draw_order = self.g.new_edge_property("int")

        self.vertex_color = self.g.new_vertex_property("string")
        for v in self.g.vertices():
            self.vertex_color[v] = 'black'

    def add_edge(self, u, v):
        e = self.g.add_edge(self.g.vertex(u), self.g.vertex(v))
        self.matched_color[e] = 'black'
        self.matched_width[e] = 1.0
        self.draw_order[e] = 0

    def switch(self, e):
        anim_edge = self.g.edge(e.to.id, e.twin.to.id)
        self.matched_color[anim_edge] = 'red' if e.matched else 'black'
        self.matched_width[anim_edge] = 4.0 if e.matched else 1.0
        self.draw_order[anim_edge] = 1 if e.matched else 0

    def color_vertices(self, vertices, color):
        for v in vertices:
            self.vertex_color[self.g.vertex(v.id)] = color

    def color_alternating(self, edges):
        for e in edges:
            if not e.matched:
                anim_edge = self.g.edge(e.to.id, e.twin.to.id)
                self.matched_color[anim_edge] = 'blue'
                self.matched_width[anim_edge] = 4.0
                self.draw_order[anim_edge] = 1

    def shrink(self, blossom):
        self.color_vertices(blossom, "red")

        old_pos = [copy.copy(self.pos[self.g.vertex(v.id)]) for v in blossom]
        center = [0, 0]
        for p in old_pos:
            for i in range(2):
                center[i] += p[i]
        for i in range(2):
            center[i] /= len(blossom) 
        for v in blossom:
            self.pos[self.g.vertex(v.id)] = center

        return old_pos
    
    def expand(self, blossom, old_pos, dsu):
        for i in range(len(blossom)):
            self.pos[self.g.vertex(blossom[i].id)] = old_pos[i]
            self.vertex_color[self.g.vertex(blossom[i].id)] \
                = "red" if isinstance(dsu.find(blossom[i]), Blossom) else "black"

    def animate(self, callback):
        self.pos = gt.sfdp_layout(self.g)
        self.win = gt.GraphWindow(self.g, self.pos, geometry=(750,600), eorder=self.draw_order,
            vertex_fill_color=self.vertex_color, edge_color=self.matched_color, 
            edge_pen_width=self.matched_width, vertex_size=20)

        self.win.connect("delete_event", Gtk.main_quit)
        self.win.graph.disconnect_by_func(self.win.graph.button_press_event)
        self.win.connect("button_press_event", callback)
        self.win.show_all()

        Gtk.main()

    def update_state(self):
        self.win.graph.regenerate_surface()
        self.win.graph.queue_draw()