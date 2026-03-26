import pygame
from config import GAME_SETTINGS

def CreateWindow():
    screen = pygame.display.set_mode((GAME_SETTINGS["window_width"], GAME_SETTINGS["window_height"]), pygame.RESIZABLE | pygame.SCALED | pygame.FULLSCREEN)
    pygame.display.set_caption("Snake Game")
    return screen