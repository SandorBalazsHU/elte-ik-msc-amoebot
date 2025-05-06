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
    def move_right(bot):
        bot.target = (bot.row, bot.col + 1)

    def random_wander(bot):
        neighbors = bot.triangle_map.get_neighbors(bot.row, bot.col)
        free = [pos for pos in neighbors if not bot.triangle_map.is_occupied(*pos)]
        if free:
            bot.target = random.choice(free)

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

    def caterpillar_behavior(bot, x=None, y=None, shift=None):
        # Inicializálás fázis
        if x is not None and y is not None and shift is not None:
            bot.tank_x = x
            bot.tank_y = y
            bot.tank_shift = shift
            bot.tank_initialized = True
            bot.tank_start_row = bot.row - shift  # eredeti sor, ahonnan indult
            return

        if not hasattr(bot, 'tank_initialized') or not bot.tank_initialized:
            return

        if not hasattr(bot, 'tank_counter'):
            bot.tank_counter = 0
            bot.tank_phase = 0
            bot.tank_position = bot.tank_shift or 0

    def caterpillar_behavior(bot, x=None, y=None, shift=None):
        # Inicializálás
        if x is not None and y is not None and shift is not None:
            bot.tank_x = x
            bot.tank_y = y
            bot.tank_shift = shift
            bot.tank_initialized = True
            bot.tank_start_row = bot.row - shift  # Indulási sor mentése
            return

        if not hasattr(bot, 'tank_initialized') or not bot.tank_initialized:
            return

        if not hasattr(bot, 'tank_counter'):
            bot.tank_counter = 0
            bot.tank_phase = 0

        # Mozgásfázisok
        if bot.tank_phase == 0:  # Jobbra
            bot.heading = 3
            bot.tank_counter += 1
            if bot.tank_counter >= bot.tank_x + 1 - bot.tank_shift:
                bot.tank_counter = 0
                bot.tank_phase = 1

        elif bot.tank_phase == 1:  # Le
            bot.heading = 5
            bot.tank_counter += 1
            if bot.tank_counter >= bot.tank_y:
                bot.tank_counter = 0
                bot.tank_phase = 2

        elif bot.tank_phase == 2:  # Balra
            bot.heading = 2
            bot.tank_counter += 1
            if bot.tank_counter >= bot.tank_x - bot.tank_shift:
                bot.tank_counter = 0
                bot.tank_phase = 3

        elif bot.tank_phase == 3:  # Fel
            bot.heading = 0
            if bot.row <= bot.tank_start_row + 1:
                bot.tank_counter = 0
                bot.tank_phase = 0
                bot.heading = 3
                bot.tank_counter += 1

        # A célpozíció kiszámítása és beállítása
        target = bot.triangle_map.get_valid_target_position(bot.row, bot.col, bot.heading)
        if target:
            bot.target = target


#EXAMPLE:
#bot.set_intelligent_behavior(center_seek_behavior)