class Level_00:
    def __init__(self):
        self.name = "Forest"
        self.speed = 5
        self.snake_start = [(500, 600)]
        self.walls = [
            (0, 0, 800, 20),      # верхняя стена
            (0, 580, 800, 20),    # нижняя стена
            (0, 0, 20, 600),      # левая стена
            (780, 0, 20, 600)     # правая стена
        ]
        self.background_color = (10, 50, 10) #Green
