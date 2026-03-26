import pygame

# =======================
#        COLORS
# =======================

COLORS = {
    "BLACK": (0, 0, 0),
    "GRAY": (128, 128, 128),
    "WHITE": (255, 255, 255),
    "YELLOW": (255, 255, 0),
    "RED": (255, 0, 0),
    "GREEN": (0, 255, 0),
    "BLUE": (0, 0, 255),
    
    # Дополнительные цвета для игры
    "DARK_GREEN": (10, 50, 10),
    "LIGHT_GREEN": (30, 90, 30),
    "ORANGE": (255, 165, 0),
    "PURPLE": (128, 0, 128),
    "CYAN": (0, 255, 255),
    "PINK": (255, 192, 203),
}


# =======================
#     SOUND SETTINGS
# =======================

SOUND_SETTINGS = {
    "background_volume": 0.5,
    "effects_volume": 0.7,
    "muted": False
}



# =======================
#     WINDOW SETTINGS
# =======================

GAME_SETTINGS = {
    "window_width": 1000,
    "window_height": 600,
}



# =======================
#   HELPER FUNCTIONS
# =======================

def get_color(name):
    """Возвращает цвет по имени"""
    return COLORS.get(name.upper(), COLORS["WHITE"])


