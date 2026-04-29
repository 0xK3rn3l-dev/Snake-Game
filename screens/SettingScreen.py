from screens.BaseScreen import BaseScreen
import pygame

class SettingScreen(BaseScreen):
    def __init__(self, screen):
        super().__init__(screen)
        
        self.exiting = False
        self.fade_alpha = 0
        self.fade_speed = 10

        # вкладки меню настроек
        self.tabs = [
            {"text": "Sound",  "y": 250, "action": "sound"},
            {"text": "Game",   "y": 320, "action": "game"},
            {"text": "Snake",  "y": 390, "action": "snake"},
        ]

        self.tab_rects = []
        self.active_tab = "sound"

        
        # змейки
        self.snake_scroll_x = 0
        self.snake_scroll_speed = 20

        self.snakes = [
            {"name": "Standard", "color": (0, 255, 255), "unlocked": True},
            {"name": "Golden",   "color": (255, 215, 0), "unlocked": True},
            {"name": "Red",      "color": (255, 0, 0), "unlocked": False},
            {"name": "Purple",   "color": (160, 32, 240), "unlocked": False},
            {"name": "Neon",     "color": (57, 255, 20), "unlocked": False},
        ]

        self.selected_snake = 0

        self._create_tab_rects()


    def _create_tab_rects(self):
        self.tab_rects = []

        for item in self.tabs:
            text_surface = self.font_medium.render(item["text"], True, self.WHITE)
            rect = text_surface.get_rect(center=(200, item["y"]))
            self.tab_rects.append(rect)




    # =======================
    #       Functions
    #========================

    def on_enter(self, data=None):
        self.exiting = False
        self.fade_alpha = 0


    def handle_events(self, events):
        mouse_pos = pygame.mouse.get_pos()

        for event in events:

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.exiting = True

            # 👉 СКРОЛЛ КОЛЁСИКОМ
            if event.type == pygame.MOUSEWHEEL and self.active_tab == "snake":
                self.snake_scroll_x += event.y * self.snake_scroll_speed

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:

                # вкладки
                for i, rect in enumerate(self.tab_rects):
                    if rect.collidepoint(mouse_pos):
                        self.active_tab = self.tabs[i]["action"]

                # выбор змеи
                if self.active_tab == "snake":
                    for i in range(len(self.snakes)):
                        box = pygame.Rect(450 + self.snake_scroll_x + i * 120, 250, 80, 80)
                        if box.collidepoint(mouse_pos):
                            if not self.snakes[i]["unlocked"]:
                                return
                            self.selected_snake = i

    def update(self):
        if self.exiting:
            self.fade_alpha += self.fade_speed

            if self.fade_alpha >= 255:
                self.next_screen = "menu"

                self.next_screen_data = {
                "selected_snake": self.selected_snake
                }

                self.running = False


        # ограничение скролла
        max_scroll = 0
        min_scroll = min(0, 450 - (len(self.snakes) * 120))
        self.snake_scroll_x = max(min_scroll, min(max_scroll, self.snake_scroll_x))

    def draw(self):
        self.screen.fill(self.BLACK)

        # заголовок
        title = self.font_title.render("SETTINGS", True, self.YELLOW)
        self.screen.blit(title, (self.screen.get_width() // 2 - title.get_width() // 2, 80))

        # вкладки
        for i, item in enumerate(self.tabs):
            is_hovered = self.tab_rects[i].collidepoint(pygame.mouse.get_pos())

            color = self.YELLOW if self.active_tab == item["action"] else self.WHITE
            font = self.font_large if is_hovered else self.font_medium

            text = font.render(item["text"], True, color)
            rect = text.get_rect(center=self.tab_rects[i].center)
            self.screen.blit(text, rect)

        # контент
        if self.active_tab == "sound":
            self._draw_sound()

        elif self.active_tab == "game":
            self._draw_game()

        elif self.active_tab == "snake":
            self._draw_snake()

        # fade
        if self.exiting:
            fade = pygame.Surface(self.screen.get_size())
            fade.fill((0, 0, 0))
            fade.set_alpha(self.fade_alpha)
            self.screen.blit(fade, (0, 0))




    # =======================
    #      draw_content
    #========================

    def _draw_sound(self):
        text = self.font_medium.render("Sound settings (placeholder)", True, self.WHITE)
        self.screen.blit(text, (450, 200))

    def _draw_game(self):
        text = self.font_medium.render("Game settings (placeholder)", True, self.WHITE)
        self.screen.blit(text, (450, 200))

    def _draw_snake(self):
        # зона, где можно рисовать змей (ограничиваем область)
        clip_rect = pygame.Rect(350, 200, self.screen.get_width() - 350, 300)

        old_clip = self.screen.get_clip()
        self.screen.set_clip(clip_rect)  # ВКЛЮЧАЕМ ОГРАНИЧЕНИЕ

        x_start = 450 + self.snake_scroll_x
        y = 250

        for i, snake in enumerate(self.snakes):

            rect = pygame.Rect(x_start + i * 120, y, 80, 80)

            is_unlocked = snake["unlocked"]

            border_color = self.YELLOW if i == self.selected_snake else self.WHITE
            pygame.draw.rect(self.screen, border_color, rect, 3)

            inner_rect = rect.inflate(-10, -10)

            if is_unlocked:
                pygame.draw.rect(self.screen, snake["color"], inner_rect)
            else:
                pygame.draw.rect(self.screen, (60, 60, 60), inner_rect)

                lock = self.font_medium.render("🔒", True, self.WHITE)
                lock_rect = lock.get_rect(center=rect.center)
                self.screen.blit(lock, lock_rect)

            name_color = self.WHITE if is_unlocked else (120, 120, 120)

            name = self.font_small.render(snake["name"], True, name_color)
            self.screen.blit(name, (rect.x, rect.y + 90))

        self.screen.set_clip(old_clip)  # ВЫКЛЮЧАЕМ ОГРАНИЧЕНИЕ