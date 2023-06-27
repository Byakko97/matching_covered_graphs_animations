import graph_tool.all as gt

from gi.repository import Gtk, GLib

class GraphAnimation:
    """Animação de um grafo"""

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

    def animate(self, callback):
        self.pos = gt.sfdp_layout(self.g)
        self.win = gt.GraphWindow(self.g, self.pos, geometry=(500,400), edge_color=self.matched)

        self.win.connect("delete_event", Gtk.main_quit)
        self.win.graph.disconnect_by_func(self.win.graph.button_press_event)
        self.win.connect("button_press_event", callback)
        self.win.show_all()

        Gtk.main()

    def update_state(self):
        self.win.graph.regenerate_surface()
        self.win.graph.queue_draw()