import graph_tool.all as gt
import copy

from gi.repository import Gtk, GLib

from src.common.blossom import Blossom
from src.animation.constants import (
    VERTEX_COLOR,
    BLOSSOM_COLOR,
    UNMATCHED_COLOR,
    EDGE_WIDTH,
    MATCHED_COLOR,
    HIGHLIGHT_WIDTH,
    HIGHLIGHT_COLOR,
)


class GraphAnimation:
    """Animação de um grafo"""

    def __init__(self, n=0):
        self.g = gt.Graph(directed=False)
        if n > 0:
            self.g.add_vertex(n)

        self.pos = None
        self.win = None

        self.edge_color = self.g.new_edge_property("string")
        self.edge_width = self.g.new_edge_property("float")
        self.draw_order = self.g.new_edge_property("int")

        self.vertex_text = self.g.new_vertex_property("string")
        self.vertex_text_color = self.g.new_vertex_property("string")
        self.vertex_color = self.g.new_vertex_property("string")
        for v in self.g.vertices():
            self.vertex_color[v] = VERTEX_COLOR
            self.vertex_text[v] = ""
            self.vertex_text_color[v] = "white"

    def add_edge(self, u, v):
        e = self.g.add_edge(self.g.vertex(u), self.g.vertex(v))
        self.edge_color[e] = UNMATCHED_COLOR
        self.edge_width[e] = EDGE_WIDTH
        self.draw_order[e] = 0

    def match_color(self, e):
        anim_edge = self.g.edge(e.to.id, e.twin.to.id)
        self.edge_color[anim_edge] = (
            MATCHED_COLOR if e.matched else UNMATCHED_COLOR
        )
        self.edge_width[anim_edge] = (
            HIGHLIGHT_WIDTH if e.matched else EDGE_WIDTH
        )
        self.draw_order[anim_edge] = 1 if e.matched else 0

    def color_edges(self, edges, color):
        for e in edges:
            anim_edge = self.g.edge(e.to.id, e.twin.to.id)
            self.edge_color[anim_edge] = color

    def color_vertices(self, vertices, color):
        for v in vertices:
            self.vertex_color[self.g.vertex(v.id)] = color

    def show_labels(self, vertices):
        for v in vertices:
            id = self.g.vertex(v.id)
            self.vertex_text[id] = str(v.color) if v.color != -1 else ""

    def color_alternating(self, path, undo=False):
        for e in path:
            if not e.matched:
                anim_edge = self.g.edge(e.to.id, e.twin.to.id)
                self.edge_color[anim_edge] = (
                    HIGHLIGHT_COLOR if not undo else UNMATCHED_COLOR
                )
                self.edge_width[anim_edge] = (
                    HIGHLIGHT_WIDTH if not undo else EDGE_WIDTH
                )
                self.draw_order[anim_edge] = 1 if not undo else 0

    def shrink(self, blossom, edges):
        self.color_vertices(blossom, BLOSSOM_COLOR)
        self.color_alternating(edges, undo=True)

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
            self.vertex_color[self.g.vertex(blossom[i].id)] = (
                BLOSSOM_COLOR if isinstance(dsu.find(blossom[i]), Blossom)
                else VERTEX_COLOR
            )

    def animate(self, callback, manual_mode, speed):
        self.pos = gt.sfdp_layout(self.g)
        self.win = gt.GraphWindow(
                    self.g, self.pos, geometry=(750, 600),
                    eorder=self.draw_order,
                    vertex_fill_color=self.vertex_color,
                    vertex_text=self.vertex_text,
                    vertex_text_color=self.vertex_text_color,
                    edge_color=self.edge_color,
                    edge_pen_width=self.edge_width,
                    vertex_size=20,
        )

        self.win.connect("delete_event", Gtk.main_quit)
        self.win.graph.disconnect_by_func(self.win.graph.button_press_event)
        if manual_mode:
            self.win.connect("button_press_event", callback)
        else:
            GLib.timeout_add(speed, callback, None, None)

        self.win.show_all()
        Gtk.main()

    def update_state(self):
        self.win.graph.regenerate_surface()
        self.win.graph.queue_draw()
