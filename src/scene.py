import pygame
import pygame_menu
import random
from enum import Enum, auto

from src.config import Config
from src.menu_button import MenuButton
from src.menu_button import StepCounterDisplay
from src.amoebot import Amoebot
from src.behaviors import AmoebotState, BehaviorType, Behavior

class SceneType(Enum):
    MENU = auto()
    RANDOM = auto()
    CONNECTED = auto()
    CENTER = auto()
    WALL = auto()
    META_MODUL = auto()
    META_MODUL_2 = auto()
    SETTINGS = auto()
    EXIT = auto()
class Scene:
    def __init__(self, simulation: 'Simulation'):
        self.FONT1 = pygame.font.SysFont(None, Config.Scene.FONT1_SIZE)
        self.FONT2 = pygame.font.SysFont(None, Config.Scene.FONT2_SIZE)
        self.simulation = simulation
        self.current_scene: SceneType = SceneType.MENU
        self.menu_object:pygame_menu.Menu = None
        self.menu_button = MenuButton(
            pygame.Rect(10, 10, 80, 30),
            self.FONT1,
            "Menü",
            lambda: self.set_scene(SceneType.MENU)
        )

        self.step_display = StepCounterDisplay(
        pos=(120, 10),
        font=self.FONT1,
        color=Config.Scene.DEFAULT_BUTTON_COLOR,
        text_color=Config.Scene.DEFAULT_BUTTON_TEXT_COLOR,
        label_color=Config.Scene.DEFAULT_TEXT_COLOR
        )
        self.step_display.setSimulation(self.simulation)

        self.scene_map = {
            SceneType.MENU: self.menu,
            SceneType.RANDOM: self.setup_random_scene,
            SceneType.CONNECTED: self.setup_connected_motion_scene,
            SceneType.CENTER: self.setup_center_motion_scene,
            SceneType.WALL: self.setup_wall_motion_scene,
            SceneType.META_MODUL: self.setup_meta_modul_motion_scene,
            SceneType.META_MODUL_2: self.setup_meta_modul_2_motion_scene,
            SceneType.SETTINGS: self.settings,
            SceneType.EXIT: self.exit
        }
    
    def set_scene(self, scene_type: SceneType):
        self.simulation.amoebots.clear()
        self.simulation.commanded_bots.clear()
        self.simulation.triangle_map.clear_occupied()
        self.current_scene = scene_type
        handler = self.scene_map.get(scene_type)
        if handler:
            handler()
        if scene_type not in {SceneType.MENU, SceneType.SETTINGS, SceneType.EXIT}:
            self.simulation.resetCounter()

    def menu(self):
        self.menu_object = pygame_menu.Menu(
        'Main menu',
            self.simulation.width,
            self.simulation.height,
            theme=pygame_menu.themes.THEME_DARK
        )
        simulations_01_menu = pygame_menu.Menu(
        "Simulations 01",
        self.simulation.width,
        self.simulation.height,
        theme=pygame_menu.themes.THEME_DARK
        )
        simulations_01_menu.add.button("Random", lambda: self.set_scene(SceneType.RANDOM))
        simulations_01_menu.add.button("Connected motion", lambda: self.set_scene(SceneType.CONNECTED))
        simulations_01_menu.add.button("To center", lambda: self.set_scene(SceneType.CENTER))
        simulations_01_menu.add.button("Wall", lambda: self.set_scene(SceneType.WALL))
        simulations_01_menu.add.button("Meta modul", lambda: self.set_scene(SceneType.META_MODUL))
        simulations_01_menu.add.button("Meta modul 2", lambda: self.set_scene(SceneType.META_MODUL_2))
        simulations_01_menu.add.button('Back', pygame_menu.events.BACK)

        simulations_02_menu = pygame_menu.Menu(
        "Simulations 02",
        self.simulation.width,
        self.simulation.height,
        theme=pygame_menu.themes.THEME_DARK
        )
        simulations_02_menu.add.button('Back', pygame_menu.events.BACK)

        self.menu_object.add.button("Simulations 01", simulations_01_menu)
        self.menu_object.add.button("Simulations 02", simulations_02_menu)
        self.menu_object.add.button("Settings", lambda: self.set_scene(SceneType.SETTINGS))
        self.menu_object.add.button("Exit", lambda: self.set_scene(SceneType.EXIT))
        self.menu_object.enable()
    
    def settings(self):
        self.menu_object = pygame_menu.Menu(
            'Settings',
            self.simulation.width,
            self.simulation.height,
            theme=pygame_menu.themes.THEME_DARK
        )
        def toggle_grid(value):
            Config.Scene.show_grid = value
        def toggle_jump_pos(value):
            Config.Scene.jump_pos = value
        self.menu_object.add.toggle_switch('Show Grid', Config.Scene.show_grid, onchange=toggle_grid, toggleswitch_id='Grid')
        self.menu_object.add.toggle_switch('Jump', Config.Scene.jump_pos, onchange=toggle_jump_pos, toggleswitch_id='Jump')
        self.menu_object.add.button('Back', lambda: self.set_scene(SceneType.MENU))
        self.menu_object.enable()

    def exit(self):
        pygame.event.post(pygame.event.Event(pygame.QUIT))

    def setup_random_scene(self):
        self.simulation.amoebots = [Amoebot(self.simulation.triangle_map, random.randint(0, Config.Grid.ROWS - 1),
                                      random.randint(0, Config.Grid.COLS - 1)) for _ in range(Config.Scene.BOT_NUMBER)]

    def setup_connected_motion_scene(self):
        BOT_NUMBER = 12
        for i in range(2, BOT_NUMBER + 1):
            bot = Amoebot(self.simulation.triangle_map, i, 2)
            bot.set_behavior(BehaviorType.TO_HEADING)
            bot.set_heading(3)
            self.simulation.amoebots.append(bot)

        for i in range(2, BOT_NUMBER + 1):
            bot = Amoebot(self.simulation.triangle_map, i, 1)
            bot.set_behavior(BehaviorType.TO_HEADING)
            bot.set_heading(3)
            self.simulation.amoebots.append(bot)

        for i in range(2, BOT_NUMBER + 1):
            bot = Amoebot(self.simulation.triangle_map, i, 0)
            bot.set_behavior(BehaviorType.TO_HEADING)
            bot.set_heading(3)
            self.simulation.amoebots.append(bot)

    def setup_center_motion_scene(self):
        self.simulation.amoebots = [Amoebot(self.simulation.triangle_map, random.randint(0, Config.Grid.ROWS - 1),
                                      random.randint(0, Config.Grid.COLS - 1)) for _ in range(Config.Scene.BOT_NUMBER)]
        for bot in self.simulation.amoebots:
            bot.set_behavior(BehaviorType.INTELLIGENT)
            bot.set_intelligent_behavior(Behavior.center_seek_behavior)
    
    def setup_meta_modul_motion_scene(self):
        bots = self.create_meta_modul(start_row=0, start_col=0, rows=4, cols=4, color=(255,0,0))
        leader = bots[3][3]
        leader.color=(100,0,0)
        leader.set_state(AmoebotState.ACTIVE)
        leader.set_behavior(BehaviorType.INTELLIGENT)
        leader.set_intelligent_behavior(Behavior.zigzag_behavior)
        self.simulation.commanded_bots.append(leader)

        bots2 = self.create_meta_modul(start_row=8, start_col=7, rows=4, cols=6, color=(255,255,0))
        leader2 = bots2[0][0]
        leader2.color=(100,100,0)
        leader2.set_state(AmoebotState.ACTIVE)
        leader2.set_behavior(BehaviorType.TO_HEADING)
        leader2.set_heading(2)
        self.simulation.commanded_bots.append(leader2)

        wall = self.create_meta_modul(start_row=6, start_col=0, rows=2, cols=6, color=(255,255,255))
        wall2 = self.create_meta_modul(start_row=0, start_col=Config.Grid.COLS-2, rows=Config.Grid.COLS, cols=2, color=(255,255,255))
    
    def setup_wall_motion_scene(self):
        wall = self.create_meta_modul(start_row=6, start_col=0, rows=2, cols=10, color=(255,255,255))
        wall2 = self.create_meta_modul(start_row=0, start_col=Config.Grid.COLS-2, rows=Config.Grid.COLS, cols=2, color=(255,255,255))
        create_random_moving_amoebots(self, count=40, x_min=0, x_max=12, y_min=0, y_max=5)
        create_random_moving_amoebots(self, count=40, x_min=0, x_max=12, y_min=8, y_max=14)

    def setup_meta_modul_2_motion_scene(self):
        bots = self.create_meta_modul(start_row=0, start_col=0, rows=4, cols=4, color=(255,30,30))
        leader = bots[3][3]
        leader.color=(100,30,30)
        leader.set_state(AmoebotState.ACTIVE)
        leader.set_behavior(BehaviorType.INTELLIGENT)
        leader.set_intelligent_behavior(Behavior.center_seek_behavior)
        self.simulation.commanded_bots.append(leader)

        bots2 = self.create_meta_modul(start_row=11, start_col=9, rows=4, cols=6, color=(255,255,30))
        leader2 = bots2[0][0]
        leader2.color=(100,100,30)
        leader2.set_state(AmoebotState.ACTIVE)
        leader2.set_behavior(BehaviorType.INTELLIGENT)
        leader2.set_intelligent_behavior(Behavior.center_seek_behavior)
        self.simulation.commanded_bots.append(leader2)

        bots3 = self.create_meta_modul(start_row=0, start_col=12, rows=3, cols=3, color=(30,30,255))
        leader3 = bots3[2][0]
        leader3.color=(30,30,100)
        leader3.set_state(AmoebotState.ACTIVE)
        leader3.set_behavior(BehaviorType.INTELLIGENT)
        leader3.set_intelligent_behavior(Behavior.center_seek_behavior)
        self.simulation.commanded_bots.append(leader3)

        #wall = self.create_meta_modul(start_row=7, start_col=7, rows=1, cols=1, color=(255,255,255))

    def create_meta_modul(self, start_row: int, start_col: int, rows: int, cols: int, color = None):
        """
        Létrehoz egy összekapcsolt NxM-es amőbotblokkot a megadott kezdőpozíciótól.
        Minden botot hozzáad a szimulációhoz, PASSIVE állapotra állít, és a megadott színt kapja.
        
        :param start_row: Kezdősor
        :param start_col: Kezdőoszlop
        :param rows: Blokk sorainak száma
        :param cols: Blokk oszlopainak száma
        :param color: Az amőbotok színe (RGB tuple)
        :return: 2D lista az amőbotokkal
        """
        bots = [[None for _ in range(cols)] for _ in range(rows)]
        for r in range(rows):
            for c in range(cols):
                bot = Amoebot(self.simulation.triangle_map, start_row + r, start_col + c)
                if color:
                    bot.color = color
                bot.set_state(AmoebotState.PASSIVE)
                bots[r][c] = bot
                self.simulation.amoebots.append(bot)
        for r in range(rows):
            for c in range(cols):
                current = bots[r][c]
                if c + 1 < cols:
                    current.connect(bots[r][c + 1])
                if r + 1 < rows:
                    current.connect(bots[r + 1][c])
        return bots

def create_random_moving_amoebots(self, count: int, x_min: int, x_max: int, y_min: int, y_max: int):
    """
    Véletlenszerűen létrehoz X darab mozgó amőbotot a megadott koordináta-tartományban.
    Minden bot ACTIVE állapotot és RANDOM viselkedést kap, véletlen kezdőirányból indulva.

    :param count: Amőbotok száma
    :param x_min: Minimum oszlop
    :param x_max: Maximum oszlop
    :param y_min: Minimum sor
    :param y_max: Maximum sor
    """
    for _ in range(count):
        col = random.randint(x_min, x_max)
        row = random.randint(y_min, y_max)
        bot = Amoebot(self.simulation.triangle_map, row, col)
        bot.set_behavior(BehaviorType.RANDOM)
        self.simulation.amoebots.append(bot)