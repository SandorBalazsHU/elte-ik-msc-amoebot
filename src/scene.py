import pygame
import pygame_menu
import random
from enum import Enum, auto

from src.config import Config
from src.menu_button import MenuButton
from src.amoebot import Amoebot

class SceneType(Enum):
    MENU = auto()
    RANDOM = auto()
    CONNECTED = auto()
    WORM = auto()
    CRAWLER = auto()
    EXIT = auto()
class Scene:
    def __init__(self, simulation: 'Simulation'):
        self.WHITE = (255, 255, 255)
        self.GRAY = (30, 30, 30)
        self.sRED = (255, 100, 100)
        self.GREEN = (100, 255, 100)
        self.BLACK = (0, 0, 0)
        self.font1 = pygame.font.SysFont(None, 30)
        self.font2 = pygame.font.SysFont(None, 15)
        self.simulation = simulation
        self.current_scene: SceneType = SceneType.MENU
        self.menu_object:pygame_menu.Menu = None
        self.menu_button = MenuButton(
            pygame.Rect(10, 10, 80, 30),
            self.font1,
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
        BOT_NUMBER = 30
        self.simulation.amoebots = [Amoebot(self.simulation.triangle_map, random.randint(0, self.simulation.GRID_ROWS - 1),
                                      random.randint(0, self.simulation.GRID_COLS - 1)) for _ in range(BOT_NUMBER)]

    def setup_connected_motion_scene(self):
        BOT_NUMBER = 12
        for i in range(1, BOT_NUMBER + 1):
            bot = Amoebot(self.simulation.triangle_map, i, 1)
            self.simulation.amoebots.append(bot)
            bot.RANDOM_HEADING = True
        for i in range(1, BOT_NUMBER + 1):
            bot = Amoebot(self.simulation.triangle_map, i, 1)
            self.simulation.amoebots.append(bot)
            bot.RANDOM_HEADING = False
        for i in range(1, BOT_NUMBER + 1):
            bot = Amoebot(self.simulation.triangle_map, i, 2)
            self.simulation.amoebots.append(bot)
            bot.RANDOM_HEADING = False

    def setup_worm_motion_scene(self):
        pass

    def setup_crawler_motion_scene(self):
        pass