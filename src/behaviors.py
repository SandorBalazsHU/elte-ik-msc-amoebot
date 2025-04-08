import random
from enum import Enum, auto
from src.config import Config

class AmoebotState(Enum):
    INACTIVE = auto()      # nem mozog és nem mozdítható
    PASSIVE = auto()       # nem mozog magától, de mozdítható
    ACTIVE = auto()        # képes dönteni és mozogni
    ONE_STEP = auto()      # egyet lép külső hatásra és megint passive

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

    def center_seek_behavior(bot):
        center_row = Config.Grid.ROWS // 2
        center_col = Config.Grid.COLS // 2
        neighbors = bot.triangle_map.get_neighbors(bot.row, bot.col)
        best = min(neighbors, key=lambda pos: (center_row - pos[0])**2 + (center_col - pos[1])**2)
        bot.target = best
        heading = bot.triangle_map.get_heading_from_direction(bot.row, bot.col, best[0], best[1])
        if heading is not None:
            bot.heading = heading    

    def zigzag_behavior(bot):
        if not hasattr(bot, "zigzag_counter"):
            bot.zigzag_counter = 0
            bot.zigzag_phase = 0
        if bot.zigzag_phase == 0:
            bot.heading = 3
        else:
            bot.heading = 5
        bot.zigzag_counter += 1
        if bot.zigzag_counter >= 2:
            bot.zigzag_counter = 0
            bot.zigzag_phase = (bot.zigzag_phase + 1) % 2
        target = bot.triangle_map.get_valid_target_position(bot.row, bot.col, bot.heading)
        if target:
            bot.target = target


#EXAMPLE:
#bot.set_intelligent_behavior(center_seek_behavior)