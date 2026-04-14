from screens.BaseScreen import BaseScreen
import pygame

class MenuScreen(BaseScreen):
    def __init__(self, screen):
        super().__init__(screen)

        '''format: text, x, y, action'''
        self.menu_items = [
            {"text":"Play",     "y": 250, "action":"game"},
            {"text":"Settings", "y": 320, "action":"settings"},
            {"text":"Exit",     "y": 390, "action":"quit"}
        ]

        self.button_rects = []


        self.background_image = None
        self._load_background()
        
        self._create_button_rects()

        #self._load_audio()

    #def _load_audio(self):
        # Фоновый звук
        #self.load_background_sound("sounds/backgrounds/menu.mp3", volume=0.5)
        #self.play_background_sound()
        
        # Звуковые эффекты
        #self.load_sound("hover", "sounds/effects/hover.wav", volume=0.3)
        #self.load_sound("click", "sounds/effects/click.wav", volume=0.5)

    def _load_background(self):
        self.background_image = pygame.image.load("images/background/backgroundMenu.png")  


    def _create_button_rects(self):
        self.button_rects = []

        for item in self.menu_items:
            text_surface = self.font_medium.render(item["text"], True, self.WHITE)
            x = item.get("x", self.screen.get_width() // 2)
            rect = text_surface.get_rect(center=(x, item["y"]))
            self.button_rects.append(rect)


    def handle_events(self, events):
        mouse_pos = pygame.mouse.get_pos()

        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    for i,rect in enumerate(self.button_rects):
                        if rect.collidepoint(mouse_pos):
                            self.next_screen = self.menu_items[i]["action"]
                            self.running = False
                            return
    
    def update(self):
        if len(self.button_rects) != len(self.menu_items):
            self._create_button_rects()
        else:
            for i,rect in enumerate(self.button_rects):
                x = self.menu_items[i].get("x", self.screen.get_width() // 2)
                y = self.menu_items[i]["y"]
                expected_center = (x, y)

                if rect.center != expected_center:
                    self._create_button_rects()
                    break

    def draw(self):
        if self.background_image:
            self.screen.blit(self.background_image, (0, 0))
        else:
            self.screen.fill(self.BLACK)

        title = self.font_title.render("SNAKE GAME", True, self.YELLOW)
        title_rect = title.get_rect(center=(self.screen.get_width() // 2, 100))
        self.screen.blit(title, title_rect)

        mouse_pos = pygame.mouse.get_pos()

        for i,item in enumerate(self.menu_items):
            is_hovered = self.button_rects[i].collidepoint(mouse_pos)

            if is_hovered:
                color = self.YELLOW
                font = self.font_large
            else:
                color = self.WHITE
                font = self.font_medium

            text = font.render(item["text"], True, color)
            text_rect = text.get_rect(center=self.button_rects[i].center)
            self.screen.blit(text, text_rect)


