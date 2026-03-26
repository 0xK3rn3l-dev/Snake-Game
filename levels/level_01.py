import pygame
from config import COLORS

class Level_01:
    def __init__(self):
        self.name = "Desert"
        self.speed = 23
        self.cell_size = 30
        self.snake_start = [(10, 10), (9, 10), (8, 10)]
        
        walls_in_cells = [
            # Вертикальные стены
            (5, 3, 1, 6),
            (10, 12, 1, 5),
            (25, 2, 1, 8),
            
            # Горизонтальные стены
            (15, 5, 6, 1),
            (22, 15, 5, 1),
        ]
        
        # Преобразуем стены из клеток в пиксели
        self.walls = []
        for wall in walls_in_cells:
            x, y, w, h = wall
            self.walls.append(pygame.Rect(
                x * self.cell_size,
                y * self.cell_size,
                w * self.cell_size,
                h * self.cell_size
            ))
        
        self.background_color = COLORS["ORANGE"]