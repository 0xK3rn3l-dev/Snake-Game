import pygame
from config import COLORS

class Level_02:
    def __init__(self):
        self.name = "City"
        self.speed = 25
        self.cell_size = 30
        self.snake_start = [(5, 10), (4, 10), (3, 10)]
        
        walls_in_cells = [
            (7, 5, 1, 10),
            (16, 3, 1, 8),
            (24, 12, 1, 6),
            (10, 15, 8, 1),
            (20, 8, 6, 1),
        ]
        
        self.walls = []
        for wall in walls_in_cells:
            x, y, w, h = wall
            self.walls.append(pygame.Rect(
                x * self.cell_size,
                y * self.cell_size,
                w * self.cell_size,
                h * self.cell_size
            ))
        
        self.background_color = COLORS["PURPLE"]