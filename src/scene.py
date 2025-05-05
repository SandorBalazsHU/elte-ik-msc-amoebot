import pygame
import pygame_menu
from enum import Enum, auto

from src.config import Config
from src.menu_button import MenuButton
from src.menu_button import StepCounterDisplay
from src.scene_library import scene_library

class SceneType(Enum):
    MENU = auto()
    RANDOM = auto()
    CONNECTED = auto()
    CENTER = auto()
    WALL = auto()
    META_MODUL = auto()
    META_MODUL_2 = auto()
    SNAKE = auto()
    CRAWLER = auto()
    SETTINGS = auto()
    EXIT = auto()
class Scene:
    def __init__(self, simulation: 'Simulation'):
        self.FONT1 = pygame.font.SysFont(None, Config.Scene.FONT1_SIZE)
        self.FONT2 = pygame.font.SysFont(None, Config.Scene.FONT2_SIZE)
        self.simulation = simulation
        self.scene_library = scene_library(self)
        self.current_scene: SceneType = SceneType.MENU
        self.menu_object:pygame_menu.Menu = None
        self.menu_button = MenuButton(
            pygame.Rect(5, 5, 80, 30),
            self.FONT1,
            "Menü",
            lambda: self.set_scene(SceneType.MENU)
        )

        self.step_display = StepCounterDisplay(
        pos=(110, 5),
        font=self.FONT2,
        color=Config.Scene.DEFAULT_BUTTON_COLOR,
        text_color=Config.Scene.DEFAULT_BUTTON_TEXT_COLOR,
        label_color=Config.Scene.DEFAULT_TEXT_COLOR
        )
        self.step_display.setSimulation(self.simulation)

        self.scene_map = {
            SceneType.MENU: self.menu,
            SceneType.RANDOM: self.scene_library.setup_random_scene,
            SceneType.CONNECTED: self.scene_library.setup_connected_motion_scene,
            SceneType.CENTER: self.scene_library.setup_center_motion_scene,
            SceneType.WALL: self.scene_library.setup_wall_motion_scene,
            SceneType.META_MODUL: self.scene_library.setup_meta_modul_motion_scene,
            SceneType.META_MODUL_2: self.scene_library.setup_meta_modul_2_motion_scene,
            SceneType.SNAKE: self.scene_library.setup_snake_scene,
            SceneType.CRAWLER: self.scene_library.setup_crawler_motion_scene,
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
        simulations_02_menu.add.button("Snake", lambda: self.set_scene(SceneType.SNAKE))
        simulations_02_menu.add.button("Crawler", lambda: self.set_scene(SceneType.CRAWLER))
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
        def toggle_replace_pos(value):
            Config.Scene.replace_pos = value
        self.menu_object.add.toggle_switch('Show Grid', Config.Scene.show_grid, onchange=toggle_grid, toggleswitch_id='Grid')
        self.menu_object.add.toggle_switch('Jump', Config.Scene.jump_pos, onchange=toggle_jump_pos, toggleswitch_id='Jump')
        self.menu_object.add.toggle_switch('Replacing', Config.Scene.replace_pos, onchange=toggle_replace_pos, toggleswitch_id='Replacing')
        self.menu_object.add.button('Back', lambda: self.set_scene(SceneType.MENU))
        self.menu_object.enable()

    def exit(self):
        pygame.event.post(pygame.event.Event(pygame.QUIT))