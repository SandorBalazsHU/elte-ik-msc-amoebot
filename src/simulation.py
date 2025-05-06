import pygame
import sys
import math
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
        self.max_step_counter = 0
        self.step_counter_running = True
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
                self.updateStepCounter()
                for commanded_bot in self.commanded_bots:
                    commanded_bot.update()
                    commanded_bot.draw(self.drawer)
                for amoebot in self.amoebots:
                    if amoebot not in self.commanded_bots:
                        did_step = amoebot.update()
                        amoebot.draw(self.drawer)
                self.scene_manager.menu_button.draw(self.screen)
                self.scene_manager.step_display.draw(self.screen)
                self.stepCounting()

            pygame.display.flip()
            self.clock.tick(Config.Window.FPS)

    def startCounter(self):
        self.step_counter_running = True
    
    def stopCounter(self):
        self.step_counter_running = False
    
    def resetCounter(self):
        self.step_counter = 0
        self.max_step_counter = 0

    def stepCounting(self):
        if not hasattr(self, "animation_progress_time"):
            self.animation_progress_time = 0.0

        # Minden frame hozzáadódik
        self.animation_progress_time += 1

        # Számoljuk ki, mennyi frame egy teljes lépés:
        idle = Config.Amoebot.IDLE_DELAY
        speed = Config.Amoebot.SPEED
        anim_frames = 2 * math.ceil(1.0 / speed)
        total_step_frames = idle + anim_frames

        while self.animation_progress_time >= total_step_frames:
            if self.step_counter_running:
                self.step_counter += 1
            self.animation_progress_time -= total_step_frames
        
    def updateStepCounter(self):
        if self.amoebots:
            self.max_step_counter = max(bot.step_counter for bot in self.amoebots)
