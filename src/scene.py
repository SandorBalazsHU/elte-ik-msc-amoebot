import pygame
import pygame_menu
import random
from enum import Enum, auto

from src.config import Config
from src.menu_button import MenuButton
from src.amoebot import Amoebot
from src.behaviors import BehaviorType, Behavior

class SceneType(Enum):
    MENU = auto()
    RANDOM = auto()
    CONNECTED = auto()
    WORM = auto()
    CRAWLER = auto()
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
            SceneType.WORM: self.setup_worm_motion_scene,
            SceneType.CRAWLER: self.setup_crawler_motion_scene,
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
        self.menu_object.add.button("Worm motion", lambda: self.set_scene(SceneType.WORM))
        self.menu_object.add.button("Crawler motion", lambda: self.set_scene(SceneType.CRAWLER))
        self.menu_object.add.button("Exit", lambda: self.set_scene(SceneType.EXIT))
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

    def setup_worm_motion_scene(self):
        BOT_NUMBER = 12
        for i in range(1, BOT_NUMBER + 1):
            bot = Amoebot(self.simulation.triangle_map, i, 3)
            bot.set_behavior(BehaviorType.INTELLIGENT)
            bot.set_intelligent_behavior(Behavior.move_right)
            self.simulation.amoebots.append(bot)

    def setup_crawler_motion_scene(self):
        pass