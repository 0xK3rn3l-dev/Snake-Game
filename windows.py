import pygame


def CreateWindow():
    screen = pygame.display.set_mode((600, 600), pygame.RESIZABLE | pygame.SCALED)
    pygame.display.set_caption("Snake Game")
    return screen