from config import COLORS


class Level_00:
    def __init__(self):
        self.name = "Forest"
        self.speed = 30
        self.cell_size = 30
        self.snake_start = [(10, 10), (9, 10), (8, 10)]
        self.walls = []
        self.background_color = COLORS["DARK_GREEN"]