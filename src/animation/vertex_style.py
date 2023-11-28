class VertexStyle():
    def __init__(self):
        self.color = "white"
        self.border_color = "black"
        self.shape = "circle"
        self.text = ""
        self.text_color = "white"


class BlossomStyle(VertexStyle):
    def __init__(self):
        super().__init__()
        self.color = "gray"


class FlowerStyle(VertexStyle):
    def __init__(self):
        super().__init__()
        self.shape = "double_circle"


class BarrierStyle(VertexStyle):
    def __init__(self):
        super().__init__()
        self.shape = "square"
        self.color = "blue"


class DeletedVertex(VertexStyle):
    def __init__(self):
        super().__init__()
        self.border_color = "gray"


class OddComponentStyle(VertexStyle):
    def __init__(self):
        super().__init__()
        self.shape = "double_circle"


class EvenComponentStyle(VertexStyle):
    def __init__(self):
        super().__init__()
        self.color = "black"
