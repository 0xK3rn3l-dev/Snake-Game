import pygame


class Screen:
    def __init__(self, screen):
        self.screen = screen
        self.running = False
        self.next_screen = None
        self.clock = pygame.time.Clock()

        #Colors
        self.BLACK = (0, 0, 0)
        self.GRAY = (128, 128, 128)
        self.WHITE = (255, 255, 255)
        self.YELLOW = (255, 255, 0)
        self.RED = (255, 0, 0)
        self.GREEN = (0, 255, 0)
        self.BLUE = (0, 0, 255)
        
        #Fonts
        self.font_small = pygame.font.Font(None, 24)
        self.font_medium = pygame.font.Font(None, 36)
        self.font_large = pygame.font.Font(None, 48)
        self.font_title = pygame.font.Font(None, 72)

        self.sounds = {}
        self.background_sound = None
        self.background_sound_volume = 0.5
        self.effects_sound_volume = 0.7

    # =======================
    #         Sounds
    #========================

    # -----------------------
    #     background_sound
    #------------------------

    def load_background_sound(self, path, volume=None):
        self.background_sound = path
        pygame.mixer.music.load(path)
        vol = volume if volume is not None else self.background_sound_volume
        pygame.mixer.music.set_volume(vol)


    def play_background_sound(self, loops=-1, fade_ms=0):
        ''' fade_ms - плавное появление в миллисекундах '''
        if fade_ms > 0:
            pygame.mixer.music.play(loops, 0, fade_ms)
        else:
            pygame.mixer.music.play(loops)


    def stop_background_sound(self, fade_ms=0):
        ''' fade_ms - плавное затухание в миллисекундах '''
        if fade_ms > 0:
            pygame.mixer.music.fadeout(fade_ms)
        else:
            pygame.mixer.music.stop()

    def pause_background_sound(self):
        pygame.mixer.music.pause()

    def unpause_background_sound(self):
        pygame.mixer.music.unpause()

    def set_background_sound_volume(self, volume):
        '''volume от 0.0 до 1.0'''
        self.background_sound_volume = max(0.0, min(1.0, volume))
        pygame.mixer.music.set_volume(self.background_sound_volume)


    # -----------------------
    #      sound effects
    #------------------------

    def load_sound(self, name, path, volume=None):
        sound = pygame.mixer.Sound(path)
        vol = volume if volume is not None else self.effects_sound_volume
        sound.set_volume(vol)
        self.sounds[name] = sound

    def play_sound(self, name, loops=0, fade_ms=0):
        if name in self.sounds:
            if fade_ms > 0:
                self.sounds[name].play(loops, fade_ms=fade_ms)
            else:
                self.sounds[name].play(loops)

    def set_sound_volume(self, name=None, volume=None):
        if volume is not None:
            self.effects_sound_volume = max(0.0, min(1.0, volume))

        if name:
            if name in self.sounds:
                vol = volume if volume is not None else self.effects_sound_volume
                self.sounds[name].set_volume(vol)
        else:
            for sound in self.sounds.values():
                sound.set_volume(self.effects_sound_volume)

    def stop_all_sounds(self):
        for sound in self.sounds.values():
            sound.stop()

    # =======================
    #          Main
    #========================

    def handle_events(self, events):
        pass

    def update(self):
        pass

    def draw(self):
        pass


class MenuScreen(Screen):
    def __init__(self, screen):
        super().__init__(screen)

        self.menu_items = [
            {"text":"Play", "x": 200, "y": 250, "action":"game"},
            {"text":"Settings", "x": 400, "y": 320, "action":"settings"},
            {"text":"Exit", "x": 600, "y": 390, "action":"quit"}
        ]

        self.button_rects = []

        self._create_button_rects()
        #self._load_audio()

    #def _load_audio(self):
        """Загружает все звуки для меню"""
        # Фоновый звук
        #self.load_background_sound("sounds/backgrounds/menu.mp3", volume=0.5)
        #self.play_background_sound()
        
        # Звуковые эффекты
        #self.load_sound("hover", "sounds/effects/hover.wav", volume=0.3)
        #self.load_sound("click", "sounds/effects/click.wav", volume=0.5)


    def _create_button_rects(self):
        self.button_rects = []

        for item in self.menu_items:
            text_surface = self.font_medium.render(item["text"], True, self.WHITE)

            x = item.get("x", self.screen.get_width() // 2)
            rect = text_surface.get_rect(center=(x, item["y"]))

            #rect = text_surface.get_rect(center=(self.screen.get_width() // 2, item["y"]))
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
                #expected_center = (self.screen.get_width() // 2, self.menu_items[i]["y"])

                if rect.center != expected_center:
                    self._create_button_rects()
                    break

    def draw(self):
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


class GameScreen(Screen):
    def __init__(self,screen):
        super().__init__(screen)

class SettingsScreen(Screen):
    def __init__(self, screen):
        super().__init__(screen)
