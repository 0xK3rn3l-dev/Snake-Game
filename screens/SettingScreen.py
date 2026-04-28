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
        self.snakes = [
            {"name": "Standard", "color": (0, 255, 255)},   # CYAN
            {"name": "Golden",   "color": (255, 215, 0)},   # YELLOW
        ]

        self.selected_snake = 0

        self._create_tab_rects()

    def _create_tab_rects(self):
        self.tab_rects = []

        for item in self.tabs:
            text_surface = self.font_medium.render(item["text"], True, self.WHITE)
            rect = text_surface.get_rect(center=(200, item["y"]))
            self.tab_rects.append(rect)

    def on_enter(self):
        self.exiting = False
        self.fade_alpha = 0

    def handle_events(self, events):
        mouse_pos = pygame.mouse.get_pos()

        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.exiting = True

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:

                # клик по вкладкам
                for i, rect in enumerate(self.tab_rects):
                    if rect.collidepoint(mouse_pos):
                        self.active_tab = self.tabs[i]["action"]

                # выбор змейки
                if self.active_tab == "snake":
                    for i in range(len(self.snakes)):
                        box = pygame.Rect(450 + i * 120, 250, 80, 80)
                        if box.collidepoint(mouse_pos):
                            self.selected_snake = i

    def update(self):
        if self.exiting:
            self.fade_alpha += self.fade_speed

            if self.fade_alpha >= 255:
                self.next_screen = "menu"
                self.running = False

    def draw(self):
        self.screen.fill(self.BLACK)

        # заголовок
        title = self.font_title.render("SETTINGS", True, self.YELLOW)
        self.screen.blit(title, (self.screen.get_width() // 2 - title.get_width() // 2, 80))

        # вкладки слева
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

        if self.exiting:
            fade = pygame.Surface(self.screen.get_size())
            fade.fill((0, 0, 0))
            fade.set_alpha(self.fade_alpha)
            self.screen.blit(fade, (0, 0))


    def _draw_sound(self):
        text = self.font_medium.render("Sound settings (placeholder)", True, self.WHITE)
        self.screen.blit(text, (450, 250))

    def _draw_game(self):
        text = self.font_medium.render("Game settings (placeholder)", True, self.WHITE)
        self.screen.blit(text, (450, 250))

    def _draw_snake(self):
        x_start = 450
        y = 250

        for i, snake in enumerate(self.snakes):
            rect = pygame.Rect(x_start + i * 120, y, 80, 80)

            # рамка
            border_color = self.YELLOW if i == self.selected_snake else self.WHITE
            pygame.draw.rect(self.screen, border_color, rect, 3)

            # цвет змейки
            inner_rect = rect.inflate(-10, -10)
            pygame.draw.rect(self.screen, snake["color"], inner_rect)

            # название
            name = self.font_small.render(snake["name"], True, self.WHITE)
            self.screen.blit(name, (rect.x, rect.y + 90))