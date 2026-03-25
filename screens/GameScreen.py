from screens.BaseScreen import BaseScreen
from levels.levelManager import LevelManager
import pygame

class GameScreen(BaseScreen):
    def __init__(self,screen):
        super().__init__(screen)

        self.level_manager = LevelManager()
        self.current_level = self.level_manager.load_level(0)

        # Игровые объекты (из уровня)
        self.snake = None
        self.foods = []
        self.walls = []
        
        # Состояние игры
        self.score = 0
        self.game_over = False

        self._load_level_objects()
    
    def _load_level_objects(self):
        """Загружает объекты из текущего уровня"""
        if self.current_level:
            self.coordinate_start_snake = self.current_level.snake_start
            self.foods = self.current_level.foods.copy()
            self.walls = self.current_level.walls
            self.speed = self.current_level.speed

    def next_level(self):
        """Переход на следующий уровень"""
        next_level = self.level_manager.next_level()
        if next_level:
            self.current_level = next_level
            self._load_level_objects()
            return True
        return False  # complete game


    def handle_events(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.next_screen = "menu"
                    self.running = False
                    return
    

    def update(self):
        if self.game_over:
            return

    def draw_ui(self):
        """Отрисовка интерфейса"""
        # Счет
        score_text = self.font_medium.render(f"Score: {self.score}", True, self.WHITE)
        self.screen.blit(score_text, (850, 20))
        
        # Уровень
        level_text = self.font_small.render(f"Level: {self.current_level.name}", True, self.GRAY)
        self.screen.blit(level_text, (20, 60))
        
        # Скорость
        speed_text = self.font_small.render(f"Speed: {self.speed}", True, self.GRAY)
        self.screen.blit(speed_text, (20, 90))
    
    def draw(self):
        # Фон уровня
        if self.current_level:
            self.screen.fill(self.current_level.background_color)
        else:
            self.screen.fill(self.BLACK)
        
        # Стены
        for wall in self.walls:
            pygame.draw.rect(self.screen, self.GRAY, wall)
        
        # Еда
        for food in self.foods:
            pygame.draw.circle(self.screen, self.RED, food, 50)
        
        # Змейка
        if self.snake:
            for segment in self.snake:
                pygame.draw.rect(self.screen, self.GREEN, (*segment, 20, 20))
        
        # Интерфейс
        self.draw_ui()
        
        if self.game_over:
            game_over_text = self.font_title.render("GAME OVER", True, self.RED)
            text_rect = game_over_text.get_rect(center=(self.screen.get_width() // 2, self.screen.get_height() // 2))
            self.screen.blit(game_over_text, text_rect)