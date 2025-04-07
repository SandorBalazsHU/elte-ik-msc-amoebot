import pygame
import pygame_menu
import random
from enum import Enum, auto

from src.config import Config
from src.menu_button import MenuButton
from src.amoebot import Amoebot
from src.behaviors import AmoebotState, BehaviorType, Behavior

class SceneType(Enum):
    MENU = auto()
    RANDOM = auto()
    CONNECTED = auto()
    CENTER = auto()
    META_MODUL = auto()
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
        self.scene_map = {
            SceneType.MENU: self.menu,
            SceneType.RANDOM: self.setup_random_scene,
            SceneType.CONNECTED: self.setup_connected_motion_scene,
            SceneType.CENTER: self.setup_center_motion_scene,
            SceneType.META_MODUL: self.setup_meta_modul_motion_scene,
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

    def menu(self):
        self.menu_object = pygame_menu.Menu(
        'Main menu',
            self.simulation.width,
            self.simulation.height,
            theme=pygame_menu.themes.THEME_DARK
        )
        self.menu_object.add.button("Random", lambda: self.set_scene(SceneType.RANDOM))
        self.menu_object.add.button("Connected motion", lambda: self.set_scene(SceneType.CONNECTED))
        self.menu_object.add.button("To center", lambda: self.set_scene(SceneType.CENTER))
        self.menu_object.add.button("Meta modul", lambda: self.set_scene(SceneType.META_MODUL))
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
        for i in range(1, BOT_NUMBER + 1):
            bot = Amoebot(self.simulation.triangle_map, i, 2)
            bot.set_behavior(BehaviorType.TO_HEADING)
            bot.set_heading(3)
            self.simulation.amoebots.append(bot)

        for i in range(1, BOT_NUMBER + 1):
            bot = Amoebot(self.simulation.triangle_map, i, 1)
            bot.set_behavior(BehaviorType.TO_HEADING)
            bot.set_heading(3)
            self.simulation.amoebots.append(bot)

        for i in range(1, BOT_NUMBER + 1):
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
        leader.set_state(AmoebotState.ACTIVE)
        leader.set_behavior(BehaviorType.INTELLIGENT)
        leader.set_intelligent_behavior(Behavior.zigzag_behavior)
        self.simulation.commanded_bots.append(leader)

        bots2 = self.create_meta_modul(start_row=8, start_col=7, rows=4, cols=6, color=(255,255,0))
        leader2 = bots2[0][0]
        leader2.set_state(AmoebotState.ACTIVE)
        leader2.set_behavior(BehaviorType.TO_HEADING)
        leader2.set_heading(2)
        self.simulation.commanded_bots.append(leader2)

        wall = self.create_meta_modul(start_row=6, start_col=0, rows=2, cols=6, color=(255,255,255))

        wall2 = self.create_meta_modul(start_row=0, start_col=Config.Grid.COLS-2, rows=Config.Grid.COLS, cols=2, color=(255,255,255))

    def create_meta_modul(self, start_row: int, start_col: int, rows: int, cols: int, color = None):
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