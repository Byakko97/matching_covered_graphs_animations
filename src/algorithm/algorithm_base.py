from src.data_structures.graph import Graph


class AlgorithmBase():

    def __init__(self, g: Graph):
        self.g = g

    def update_state(self, widget, event) -> bool:
        return False

    def run_algorithm(self) -> None:
        while self.update_state(None, None):
            pass

    def animate(self, manual_mode: bool, frequence: int) -> None:
        self.g.animation.animate(self.update_state, manual_mode, frequence)

    def run(self) -> None:
        self.run_algorithm()

    def test(self) -> None:
        self.run_algorithm()
