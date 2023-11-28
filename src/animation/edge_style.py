class EdgeStyle():
    def __init__(self):
        self.color = "black"
        self.width = 1
        self.draw_order = 0
        self.dash_style = []
        self.marker = "none"


class MatchingStyle(EdgeStyle):
    def __init__(self):
        super().__init__()
        self.color = "red"
        self.width = 5
        self.draw_order = 1


class AlternatingStyle(EdgeStyle):
    def __init__(self):
        super().__init__()
        self.color = "blue"
        self.width = 4
        self.draw_order = 1
        self.dash_style = [0.2, 0.15, 0]


class DeletedEdge(EdgeStyle):
    def __init__(self):
        super().__init__()
        self.color = "gray"
        self.dash_style = [0.1, 0.05, 0]


class NotMatchableStyle(EdgeStyle):
    def __init__(self):
        super().__init__()
        self.marker = "bar"
        self.color = "blue"
        self.width = 2
