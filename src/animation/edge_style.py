class EdgeStyle():
    def __init__(self):
        self.color = "black"
        self.width = 1
        self.draw_order = 0
        self.dash_style = []


class MatchingStyle(EdgeStyle):
    def __init__(self):
        super().__init__()
        self.color = "red"
        self.width = 4
        self.draw_order = 1


class AlternatingStyle(EdgeStyle):
    def __init__(self):
        super().__init__()
        self.color = "blue"
        self.width = 4
        self.draw_order = 1
        self.dash_style = [0.2, 0.15, 0]
