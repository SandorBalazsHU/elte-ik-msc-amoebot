import pygame
import sys

from src.config import Config
from src.scene import Scene, SceneType
from src.triangle_map import TriangleMap
from src.drawer import AntiAliasedDrawer

class Simulation:
    def __init__(self):
        self.width, self.height = Config.Window.WIDTH, Config.Window.HEIGHT
        self.screen = None
        self.clock = None
        self.triangle_map: TriangleMap = None
        self.commanded_bots = []
        self.amoebots = []
        self.drawer: AntiAliasedDrawer = None
        self.scene_manager: Scene = None
        self.grid_surface = None
        self.step_counter = 0
        self.step_counter_running = True
        self.step_check_enabled = True
        self.init()

    def init(self):
        pygame.init()
        self.scene_manager = Scene(self)
        self.triangle_map = TriangleMap()
        self.width, self.height = self.triangle_map.get_window_size()
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption(Config.Window.CAPTION)
        icon = pygame.image.load(Config.Window.ICON_PATH)
        pygame.display.set_icon(icon)
        self.drawer = AntiAliasedDrawer(self.screen)
        self.clock = pygame.time.Clock()
        self.scene_manager.set_scene(SceneType.MENU)
        self.grid_surface = self.triangle_map.create_grid_surface(self.width,self.height)

    def start(self):
        while True:
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if self.scene_manager.current_scene != SceneType.MENU:
                    self.scene_manager.step_display.handle_event(event)
                    if self.scene_manager.menu_button.handle_event(event):
                        self.scene_manager.set_scene(SceneType.MENU)

            self.screen.fill(Config.Window.BACKGROUND_COLOR)

            if self.scene_manager.current_scene in {SceneType.MENU, SceneType.SETTINGS}:
                if self.scene_manager.menu_object.is_enabled():
                    self.scene_manager.menu_object.update(events)
                    self.scene_manager.menu_object.draw(self.screen)
            else:
                if Config.Scene.show_grid:
                    self.screen.blit(self.grid_surface, (0, 0))
                for commanded_bot in self.commanded_bots:
                    commanded_bot.update()
                    commanded_bot.draw(self.drawer)
                for amoebot in self.amoebots:
                    if amoebot not in self.commanded_bots:
                        did_step = amoebot.update()
                        self.updateCounter(did_step)
                        amoebot.draw(self.drawer)
                self.scene_manager.menu_button.draw(self.screen)
                self.scene_manager.step_display.draw(self.screen)

            pygame.display.flip()
            self.clock.tick(Config.Window.FPS)

    def startCounter(self):
        self.step_counter_running = True
    
    def stopCounter(self):
        self.step_counter_running = False
    
    def resetCounter(self):
        self.step_counter = 0

    def updateCounter(self, did_step):
        if self.step_counter_running and self.step_check_enabled and did_step:
            self.step_counter += 1
            self.step_check_enabled = False  # blokkoljuk a számlálást, amíg nem jön egy False
        elif not did_step:
            self.step_check_enabled = True  # újra engedélyezzük, ha nem lépett