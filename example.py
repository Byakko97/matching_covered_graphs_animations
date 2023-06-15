from graph_tool.all import *
from random import randint
import time

class grafo():

        def __init__(self):
                self.g = Graph(directed = False)

                self.vertices = []
                self.color = self.g.new_vertex_property("string")
                for i in range(10):
                        self.vertices.append(self.g.add_vertex())
                        self.color[self.vertices[i]] = 'black'

                for i in range(10):
                        for j in range(i + 2, 10, 2):
                                self.g.add_edge(self.vertices[i], self.vertices[j])

                self.win = None

        def animate(self, last=False):
                i = self.vertices[randint(0, 9)]
                self.color[i] = 'black' if self.color[i] == 'red' else 'black'

                self.win = graph_draw(self.g, vertex_color=self.color, window=self.win, return_window=True, main=last)
                time.sleep(0.5)

g = grafo()

for i in range(10):
       g.animate()

g.animate(True)