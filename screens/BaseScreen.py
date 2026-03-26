import pygame
from config import COLORS, SOUND_SETTINGS  

class BaseScreen:
    def __init__(self, screen):
        
        #Main
        self.screen = screen
        self.running = False
        self.next_screen = None
        self.clock = pygame.time.Clock()

        # Colors (из конфига)
        self.colors = COLORS

        self.BLACK = COLORS["BLACK"]
        self.WHITE = COLORS["WHITE"]
        self.GRAY = COLORS["GRAY"]
        self.YELLOW = COLORS["YELLOW"]
        self.RED = COLORS["RED"]
        self.GREEN = COLORS["GREEN"]
        
        #Fonts
        self.font_small = pygame.font.Font(None, 24)
        self.font_medium = pygame.font.Font(None, 36)
        self.font_large = pygame.font.Font(None, 48)
        self.font_title = pygame.font.Font(None, 72)

        #Sounds
        self.sounds = {}
        self.background_sound = None
        self.background_sound_volume = SOUND_SETTINGS["background_volume"]
        self.effects_sound_volume = SOUND_SETTINGS["effects_volume"]


    # =======================
    #          Main
    #========================

    def handle_events(self, events):
        pass

    def update(self):
        pass

    def draw(self):
        pass


    # -----------------------
    #     background_sound
    #------------------------

    def load_background_sound(self, path, volume=None):
        self.background_sound = path
        pygame.mixer.music.load(path)
        vol = volume if volume is not None else self.background_volume
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
        self.background_volume = max(0.0, min(1.0, volume))
        pygame.mixer.music.set_volume(self.background_volume)


    # -----------------------
    #      sound effects
    #------------------------

    def load_sound(self, name, path, volume=None):
        sound = pygame.mixer.Sound(path)
        vol = volume if volume is not None else self.effects_volume
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
            self.effects_volume = max(0.0, min(1.0, volume))
        if name:
            if name in self.sounds:
                vol = volume if volume is not None else self.effects_volume
                self.sounds[name].set_volume(vol)
        else:
            for sound in self.sounds.values():
                sound.set_volume(self.effects_volume)

    def stop_all_sounds(self):
        for sound in self.sounds.values():
            sound.stop()
