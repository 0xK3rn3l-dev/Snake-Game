import pygame
from window import CreateWindow
from core import RunningProgram  

def main():
    pygame.init()
    
    MainScreen = CreateWindow()
    RunningProgram(MainScreen)


if __name__ == '__main__':
    main()

