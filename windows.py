import pygame


def CreateWindow():
    screen = pygame.display.set_mode((1000, 600), pygame.RESIZABLE | pygame.SCALED | pygame.FULLSCREEN)
    pygame.display.set_caption("Snake Game")
    return screen