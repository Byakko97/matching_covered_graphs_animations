class AlgorithmBase():

    def __init__(self, g):
        self.g = g

    def update_state(self, widget, event):
        return False

    def run_algorithm(self):
        while self.update_state(None, None):
            pass

    def animate(self, manual_mode, speed):
        self.g.animation.animate(self.update_state, manual_mode, speed)

    def run(self):
        self.run_algorithm()

    def test(self):
        self.run_algorithm()
