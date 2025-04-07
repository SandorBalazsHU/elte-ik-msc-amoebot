import random
from enum import Enum, auto
from src.config import Config

class BehaviorType(Enum):
    RANDOM = auto()
    STAY = auto()
    TO_HEADING = auto()
    INTELLIGENT = auto()

class Behavior:
    def move_right(self):
        self.target = (self.row, self.col + 1)

    def random_wander(self):
        neighbors = self.triangle_map.get_neighbors(self.row, self.col)
        free = [pos for pos in neighbors if not self.triangle_map.is_occupied(*pos)]
        if free:
            self.target = random.choice(free)

    def stay_put(self):
        #NOT GOOD
        self.target = (self.row, self.col)

    def center_seek_behavior(bot):
        center_row = Config.Grid.ROWS // 2
        center_col = Config.Grid.COLS // 2
        neighbors = bot.triangle_map.get_neighbors(bot.row, bot.col)
        best = min(neighbors, key=lambda pos: (center_row - pos[0])**2 + (center_col - pos[1])**2)
        bot.target = best

#EXAMPLE:
#bot.set_intelligent_behavior(center_seek_behavior)