from screens.BaseScreen import BaseScreen
import pygame

class GameScreen(BaseScreen):
    def __init__(self,screen):
        super().__init__(screen)



        self.gameScreen_items = [
            {"item": "counter_foods", "y": 100},
            {"item": "level"}
        ]