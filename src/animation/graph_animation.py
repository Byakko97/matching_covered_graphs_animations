
from __future__ import annotations
from typing import List, TYPE_CHECKING
import copy

import graph_tool.all as gt
from gi.repository import Gtk, GLib

from src.animation.edge_style import EdgeStyle, MatchingStyle, AlternatingStyle
from src.animation.vertex_style import VertexStyle, BlossomStyle
from src.data_structures.blossom import Blossom
if TYPE_CHECKING:
    from src.data_structures.edge import Edge
    from src.data_structures.vertex import Vertex
    from src.data_structures.union_find import UnionFind


class GraphAnimation:
    """Animação de um grafo"""
    def __init__(self, n: int = 0):
        self.g = gt.Graph(directed=False)
        if n > 0:
            self.g.add_vertex(n)

        self.frame_count = 0
        self.offscreen = None
        self.pos = None
        self.win = None

        self.edge_color = self.g.new_edge_property("string")
        self.edge_width = self.g.new_edge_property("float")
        self.draw_order = self.g.new_edge_property("int")
        self.dash_style = self.g.new_edge_property("vector<double>")
        self.edge_marker = self.g.new_edge_property("string")

        self.vertex_color = self.g.new_vertex_property("string")
        self.vertex_border_color = self.g.new_vertex_property("string")
        self.vertex_shape = self.g.new_vertex_property("string")
        for v in self.g.vertices():
            self.set_vertex_style(v, VertexStyle())

    def add_edge(self, u: int, v: int) -> None:
        e = self.g.add_edge(self.g.vertex(u), self.g.vertex(v))
        self.set_edge_style(e, EdgeStyle())

    def set_edge_style(self, e: Edge, style: EdgeStyle) -> None:
        self.edge_color[e] = style.color
        self.edge_width[e] = style.width
        self.draw_order[e] = style.draw_order
        self.dash_style[e] = style.dash_style
        self.edge_marker[e] = style.marker

    def set_edges_style(self, edges: List[Edge], style: EdgeStyle) -> None:
        for e in edges:
            anim_edge = self.g.edge(e.to.id, e.twin.to.id)
            self.set_edge_style(anim_edge, style)

    def match_style(self, e: Edge) -> None:
        anim_edge = self.g.edge(e.to.id, e.twin.to.id)
        self.set_edge_style(
            anim_edge, MatchingStyle() if e.matched else EdgeStyle()
        )

    def set_vertex_style(self, vertex: gt.Vertex, style: VertexStyle) -> None:
        self.vertex_color[vertex] = style.color
        self.vertex_border_color[vertex] = style.border_color
        self.vertex_shape[vertex] = style.shape

    def set_vertices_style(
        self, vertices: List[Vertex], style: VertexStyle,
    ) -> None:
        for v in vertices:
            self.set_vertex_style(self.g.vertex(v.id), style)

    def color_alternating(self, path: List[Edge], undo: bool = False) -> None:
        style = AlternatingStyle() if not undo else EdgeStyle()
        alternating_edges = filter(lambda e: not e.matched, path)
        self.set_edges_style(alternating_edges, style)

    def shrink(self, blossom: Blossom, edges: List[Edge]) -> None:
        self.set_vertices_style(blossom, BlossomStyle())
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

    def expand(self, blossom: Blossom, old_pos, dsu: UnionFind) -> None:
        for i in range(len(blossom)):
            vertex = self.g.vertex(blossom[i].id)
            self.pos[vertex] = old_pos[i]
            style = (
                BlossomStyle() if isinstance(dsu.find(blossom[i]), Blossom)
                else VertexStyle()
            )
            self.set_vertex_style(vertex, style)

    def animate(
        self, callback, manual_mode: bool, frequence: int, offscreen: bool,
    ) -> None:
        self.offscreen = offscreen

        self.pos = gt.sfdp_layout(self.g)
        if not offscreen:
            self.win = gt.GraphWindow(
                        self.g, self.pos, geometry=(750, 600),
                        eorder=self.draw_order,
                        vertex_fill_color=self.vertex_color,
                        vertex_color=self.vertex_border_color,
                        vertex_shape=self.vertex_shape,
                        edge_color=self.edge_color,
                        edge_pen_width=self.edge_width,
                        edge_dash_style=self.dash_style,
                        edge_mid_marker=self.edge_marker,
                        vertex_size=20,
            )
        else:
            self.win = Gtk.OffscreenWindow()
            self.win.set_default_size(750, 600)
            self.win.graph = gt.GraphWidget(
                        self.g, self.pos,
                        eorder=self.draw_order,
                        vertex_fill_color=self.vertex_color,
                        vertex_color=self.vertex_border_color,
                        vertex_shape=self.vertex_shape,
                        edge_color=self.edge_color,
                        edge_pen_width=self.edge_width,
                        edge_dash_style=self.dash_style,
                        edge_mid_marker=self.edge_marker,
                        vertex_size=20,
            )
            self.win.add(self.win.graph)

        self.win.connect("delete_event", Gtk.main_quit)
        self.win.graph.disconnect_by_func(
            self.win.graph.button_press_event,
        )
        if manual_mode:
            self.win.connect("button_press_event", callback)
        elif offscreen:
            GLib.idle_add(callback, None, None)
        else:
            GLib.timeout_add(frequence, callback, None, None)

        self.win.show_all()
        Gtk.main()

    def update_state(self) -> None:
        self.win.graph.regenerate_surface()
        self.win.graph.queue_draw()

        if self.offscreen:
            pixbuf = self.win.get_pixbuf()
            pixbuf.savev(
                r'./frames/anim%06d.png' % self.frame_count, 'png', [], [],
            )
            self.frame_count += 1
