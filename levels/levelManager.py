from levels.level_00 import Level_00
from levels.level_01 import Level_01
from levels.level_02 import Level_02

class LevelManager:
    LEVELS = {
        0: Level_00,
        1: Level_01,
        2: Level_02
    }

    def __init__(self):
        self.current_level_num = 0
        self.current_level = None

    def load_level(self, level_num):
        if level_num in self.LEVELS:
            self.current_level = self.LEVELS[level_num]()
            self.current_level_num = level_num
            return self.current_level
        return None

    def next_level(self):
        next_num = self.current_level_num + 1
        if next_num in self.LEVELS:
            return self.load_level(next_num)
        return None #Complete game 