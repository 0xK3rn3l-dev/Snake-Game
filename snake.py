import pygame
from pygame.math import Vector2

class BaseSnake:
    def __init__(self, color, start_positions, cell_size=20):
        self.body = [Vector2(pos[0], pos[1]) for pos in start_positions]
        self.color = color
        self.direction = Vector2(1, 0)
        self.new_direction = Vector2(1, 0)
        self.cell_size = cell_size
        self.grow_flag = False

    def move(self):
        self.direction = self.new_direction
        new_head = self.body[0] + self.direction
        self.body.insert(0, new_head)

        if not self.grow_flag:
            self.body.pop()
        else:
            self.grow_flag = False

    def grow(self):
        self.grow_flag = True

    def change_direction(self, new_direction):
        # Запрещаем движение назад
        if (new_direction.x != -self.direction.x or 
            new_direction.y != -self.direction.y):
            self.new_direction = new_direction


    def check_collision(self, walls, width, height):
        head = self.body[0]
        # Столкновение со стенами
        if head.x < 0 or head.x >= width or head.y < 0 or head.y >= height:
            return True
            
        # Столкновение с препятствиями
        for wall in walls:
            wall_rect = pygame.Rect(wall)
            head_rect = pygame.Rect(head.x * self.cell_size, 
                                    head.y * self.cell_size, 
                                    self.cell_size, self.cell_size)
            if head_rect.colliderect(wall_rect):
                return True
                
        # Столкновение с собой
        if head in self.body[1:]:
            return True
            
        return False
    
    def check_food_collision(self, food_pos):
        return self.body[0] == Vector2(food_pos[0], food_pos[1])


    def draw(self, screen):
        """Отрисовка змейки"""
        for i, segment in enumerate(self.body):
            x = int(segment.x * self.cell_size)
            y = int(segment.y * self.cell_size)
            
            # Голова рисуется другим цветом
            if i == 0:
                color = (50, 255, 50)  # Ярко-зеленый для головы
            else:
                color = self.color
                
            rect = pygame.Rect(x, y, self.cell_size, self.cell_size)
            pygame.draw.rect(screen, color, rect)
            pygame.draw.rect(screen, (0, 100, 0), rect, 2)  # Контур


class StandardSnake(BaseSnake):
    def __init__(self, start_positions, cell_size=20):
        super().__init__((0, 255, 0), start_positions, cell_size)