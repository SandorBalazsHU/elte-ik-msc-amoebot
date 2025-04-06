import pygame
import sys

from src.config import Config
from src.scene import Scene, SceneType
from src.triangle_map import TriangleMap
from src.drawer import AntiAliasedDrawer

class Simulation:
    def __init__(self):
        self.width, self.height = 800, 600
        self.BACKGROUND_COLOR = (30, 30, 30)
        self.GRID_COLOR = (80, 80, 80)
        self.NODE_COLOR = (180, 180, 180)
        self.NODE_RADIUS = 5
        self.EDGE_WIDTH = 1
        self.FPS = 30
        self.GRID_ROWS = 15
        self.GRID_COLS = 15
        self.NODE_DISTANCE = 50
        self.screen = 0
        self.clock = 0
        self.triangle_map = []
        self.amoebots = []
        self.drawer: AntiAliasedDrawer = None
        self.scene_manager: Scene = None
        self.grid_surface = None
        self.init()

    def init(self):
        pygame.init()
        self.scene_manager = Scene(self)
        self.triangle_map = TriangleMap(self.GRID_ROWS, self.GRID_COLS, self.NODE_DISTANCE)
        size = self.triangle_map.get_window_size()
        self.width = size[0]
        self.height = size[1]
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Amoebot simulator 🦠 v0.7")
        icon = pygame.image.load("src/assets/icon.png")
        pygame.display.set_icon(icon)
        self.drawer = AntiAliasedDrawer(self.screen)
        self.clock = pygame.time.Clock()
        self.scene_manager.set_scene(SceneType.MENU)
        self.grid_surface = self.triangle_map.create_grid_surface(
        self.triangle_map.triangle_grid,
        self.triangle_map.get_neighbors,
        self.NODE_COLOR,
        self.GRID_COLOR,
        self.NODE_RADIUS,
        self.EDGE_WIDTH,
        self.width,
        self.height
        )

    def start(self):
        while True:
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if self.scene_manager.current_scene != SceneType.MENU:
                    if self.scene_manager.menu_button.handle_event(event):
                        self.scene_manager.set_scene(SceneType.MENU)

            self.screen.fill(self.BACKGROUND_COLOR)

            if self.scene_manager.current_scene == SceneType.MENU:
                if self.scene_manager.menu_object.is_enabled():
                    self.scene_manager.menu_object.update(events)
                    self.scene_manager.menu_object.draw(self.screen)
            else:
                self.screen.blit(self.grid_surface, (0, 0))
                for amoebot in self.amoebots:
                    amoebot.update()
                    amoebot.draw(self.drawer)
                self.scene_manager.menu_button.draw(self.screen)

            pygame.display.flip()
            self.clock.tick(self.FPS)