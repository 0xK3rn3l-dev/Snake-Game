from screens.BaseScreen import BaseScreen
from levels.levelManager import LevelManager
from snake import StandardSnake
import random
import pygame


class GameScreen(BaseScreen):
    def __init__(self,screen):
        super().__init__(screen)

        self.level_manager = LevelManager()
        self.current_level = self.level_manager.load_level(0)

        # Игровые параметры
        self.cell_size = 30
        self.grid_width = screen.get_width() // self.cell_size
        self.grid_height = screen.get_height() // self.cell_size
        
        # Игровые объекты
        self.snake = None
        self.foods = []
        self.walls = []

        # Состояние игры
        self.score = 0
        self.game_over = False
        self.game_complete = False
        self.level_complete = False
        self.move_timer = 0

        self._load_level_objects()
    
    def _load_level_objects(self):
        """Загружает объекты из текущего уровня"""
        if self.current_level:
            snake_positions = []
            for pos in self.current_level.snake_start:
                # Преобразуем пиксельные координаты в координаты сетки
                grid_x = pos[0] // self.cell_size
                grid_y = pos[1] // self.cell_size
                snake_positions.append((grid_x, grid_y))
            
            self.snake = StandardSnake(snake_positions, self.cell_size)
            
            self.walls = []
            for wall in self.current_level.walls:
                self.walls.append(wall)
            
            self.foods = []
            if hasattr(self.current_level, 'foods'):
                for food_pos in self.current_level.foods:
                    self.foods.append(food_pos)
            else:
                self._spawn_food()
                
            self.speed = self.current_level.speed


    def _spawn_food(self):
        """Создает новую еду в случайном месте"""
        while True:
            x = random.randint(0, self.grid_width - 1)
            y = random.randint(0, self.grid_height - 1)
            food_pos = (x, y)
            
            # Проверяем, не на змейке ли
            collision = False
            for segment in self.snake.body:
                if (segment.x, segment.y) == food_pos:
                    collision = True
                    break
                    
            # Проверяем, не на стене ли
            food_rect = pygame.Rect(x * self.cell_size, y * self.cell_size, 
                                   self.cell_size, self.cell_size)
            for wall in self.walls:
                if food_rect.colliderect(wall):
                    collision = True
                    break
                    
            if not collision:
                self.foods.append(food_pos)
                break



    def next_level(self):
        """Переход на следующий уровень"""
        next_level = self.level_manager.next_level()
        if next_level:
            self.current_level = next_level
            self._load_level_objects()
            self.score = 0
            self.game_over = False
            self.level_complete = False
            return True
        
        self.game_complete = True
        self.level_complete = False
        self.game_over = False
        return False  # complete game


    def handle_events(self, events):
        for event in events:

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.next_screen = "menu"
                    self.running = False
                    return
                
                if self.level_complete:
                    if event.key == pygame.K_SPACE:
                        self.next_level()
                    return
                
                # Если игра полностью пройдена
                if self.game_complete:
                    if event.key == pygame.K_SPACE:
                        self.next_screen = "menu"
                        self.running = False
                    return


                elif not self.game_over:
                    if event.key == pygame.K_UP or event.key == pygame.K_w:
                        self.snake.change_direction(pygame.math.Vector2(0, -1))
                    elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
                        self.snake.change_direction(pygame.math.Vector2(0, 1))
                    elif event.key == pygame.K_LEFT or event.key == pygame.K_a:
                        self.snake.change_direction(pygame.math.Vector2(-1, 0))
                    elif event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                        self.snake.change_direction(pygame.math.Vector2(1, 0))
                    elif event.key == pygame.K_r and not self.game_over:
                        # Перезапуск уровня
                        self._load_level_objects()
                        self.score = 0
                        self.game_over = False

                elif event.key == pygame.K_r and self.game_over:
                    # Перезапуск при game over
                    self._load_level_objects()
                    self.score = 0
                    self.game_over = False
    

    def update(self):

        if self.level_complete or self.game_over or self.game_complete:
            return
        
        # Контроль скорости движения
        self.move_timer += 1
        if self.move_timer >= (60 // self.speed):
            self.move_timer = 0
            
            self.snake.move()
            
            for food in self.foods[:]: 
                if self.snake.check_food_collision(food):
                    self.foods.remove(food)
                    self.snake.grow()
                    self.score += 10
                    self._spawn_food()
                    
                    if self.score >= 100:
                        self.level_complete = True

            if self.snake.check_collision(self.walls, self.grid_width, self.grid_height):
                self.game_over = True


    # =======================
    #         Draw
    #========================

    def draw_ui(self):
        """Отрисовка интерфейса"""
        # Счет
        score_text = self.font_medium.render(f"Score: {self.score}", True, self.WHITE)
        self.screen.blit(score_text, (self.screen.get_width() - 150, 20))
        
        # Уровень
        if self.current_level:
            level_text = self.font_small.render(f"Level: {self.current_level.name}", True, self.GRAY)
            self.screen.blit(level_text, (20, 20))
            
            # Скорость
            speed_text = self.font_small.render(f"Speed: {self.speed}", True, self.GRAY)
            self.screen.blit(speed_text, (20, 50))
    
        # Подсказка
        hint_text = self.font_small.render("ESC - Menu | R - Restart", True, self.GRAY)
        self.screen.blit(hint_text, (20, self.screen.get_height() - 30))


    def draw(self):
        # Фон уровня
        if self.current_level:
            self.screen.fill(self.current_level.background_color)
        else:
            self.screen.fill(self.BLACK)

        self._draw_grid()

        # Стены
        for wall in self.walls:
            pygame.draw.rect(self.screen, self.GRAY, wall)
        
        # Еда
        for food in self.foods:
            x = food[0] * self.cell_size
            y = food[1] * self.cell_size
            pygame.draw.circle(self.screen, self.RED, 
                             (x + self.cell_size//2, y + self.cell_size//2), 
                             self.cell_size//2 - 2)
        
        # Змейка
        if self.snake:
            self.snake.draw(self.screen)
        
        # Интерфейс
        self.draw_ui()
        

        # =======================
        #      Surface text
        # =======================

        # Level complete
        if self.level_complete:
            overlay = pygame.Surface(self.screen.get_size())
            overlay.set_alpha(128)
            overlay.fill(self.BLACK)
            self.screen.blit(overlay, (0, 0))

            level_complete_text = self.font_title.render("LEVEL COMPLETE", True, self.GREEN)
            text_level_rect = level_complete_text.get_rect(center=(self.screen.get_width() // 2, 
                                                        self.screen.get_height() // 2 - 40))
            self.screen.blit(level_complete_text, text_level_rect)

            complete_level_text = self.font_medium.render("Press SPACE for next level", True, self.WHITE)
            complete_level_rect = complete_level_text.get_rect(center=(self.screen.get_width() // 2, 
                                                         self.screen.get_height() // 2 + 20))
            self.screen.blit(complete_level_text, complete_level_rect)


        # Game complete
        if self.game_complete:
            overlay = pygame.Surface(self.screen.get_size())
            overlay.set_alpha(128)
            overlay.fill(self.BLACK)
            self.screen.blit(overlay, (0, 0))

            game_complete_text = self.font_title.render("GAME COMPLETE!", True, self.GREEN)
            text_game_rect = game_complete_text.get_rect(center=(self.screen.get_width() // 2, 
                                                        self.screen.get_height() // 2 - 40))
            self.screen.blit(game_complete_text, text_game_rect)

            complete_text = self.font_medium.render("Press SPACE to return to menu", True, self.WHITE)
            complete_rect = complete_text.get_rect(center=(self.screen.get_width() // 2, 
                                                         self.screen.get_height() // 2 + 20))
            self.screen.blit(complete_text, complete_rect)


        # Game over
        if self.game_over:
            overlay = pygame.Surface(self.screen.get_size())
            overlay.set_alpha(128)
            overlay.fill(self.BLACK)
            self.screen.blit(overlay, (0, 0))
            
            game_over_text = self.font_title.render("GAME OVER", True, self.RED)
            text_rect = game_over_text.get_rect(center=(self.screen.get_width() // 2, 
                                                        self.screen.get_height() // 2 - 40))
            self.screen.blit(game_over_text, text_rect)
            
            restart_text = self.font_medium.render("Press R to restart", True, self.WHITE)
            restart_rect = restart_text.get_rect(center=(self.screen.get_width() // 2, 
                                                         self.screen.get_height() // 2 + 20))
            self.screen.blit(restart_text, restart_rect)



    def _draw_grid(self):
        """Отрисовка сетки только в пределах игровой области"""
        game_width = (self.grid_width) * self.cell_size
        game_height = (self.grid_height) * self.cell_size

        for x in range(0, game_width + 1, self.cell_size):
            pygame.draw.line(self.screen, (30, 30, 30), (x, 0), (x, game_height))

        for y in range(0, game_height + 1, self.cell_size):
            pygame.draw.line(self.screen, (30, 30, 30), (0, y), (game_width, y))
