import pygame

from src.config import Config

class MenuButton:
    def __init__(self, rect: pygame.Rect, font: pygame.font.Font, label: str, callback,
                  color=Config.Scene.DEFAULT_BUTTON_COLOR, text_color=Config.Scene.DEFAULT_BUTTON_TEXT_COLOR):
        self.rect = rect
        self.font = font
        self.label = label
        self.callback = callback
        self.color = color
        self.text_color = text_color

    def draw(self, surface):
        pygame.draw.rect(surface, self.color, self.rect, border_radius=5)
        text_surf = self.font.render(self.label, True, self.text_color)
        text_rect = text_surf.get_rect(center=self.rect.center)
        surface.blit(text_surf, text_rect)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and self.rect.collidepoint(event.pos):
            self.callback()

class StepCounterDisplay:
    def __init__(self, pos: tuple[int, int], font: pygame.font.Font, 
                 color=Config.Scene.DEFAULT_BUTTON_COLOR, 
                 text_color=Config.Scene.DEFAULT_BUTTON_TEXT_COLOR,
                 label_color=Config.Scene.DEFAULT_TEXT_COLOR):
        self.x, self.y = pos
        self.font = font
        self.color = color
        self.text_color = text_color
        self.label_color = label_color
        self.simulation = None
        self.step_count = 0

        # Gombok létrehozása (később hivatkozunk rájuk)
        self.buttons = {
            'Start': pygame.Rect(self.x + 150, self.y, 60, 30),
            'Stop': pygame.Rect(self.x + 220, self.y, 60, 30),
            'Reset': pygame.Rect(self.x + 290, self.y, 60, 30)
        }

    def setSimulation(self, simulation):
        self.simulation = simulation

    def draw(self, surface):
        # Lépésszámláló címke
        label = self.font.render("Step counter", True, self.label_color)
        surface.blit(label, (self.x, self.y))

        # Gombok rajzolása
        for name, rect in self.buttons.items():
            pygame.draw.rect(surface, self.color, rect, border_radius=5)
            text_surf = self.font.render(name, True, self.text_color)
            text_rect = text_surf.get_rect(center=rect.center)
            surface.blit(text_surf, text_rect)

        # Lépésszám érték kirajzolása
        step_text = self.font.render(f"Steps: {self.simulation.step_counter}", True, self.label_color)
        surface.blit(step_text, (self.x + 370, self.y))

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            pos = event.pos
            if not self.simulation:
                return
            if self.buttons['Start'].collidepoint(pos):
                self.simulation.startCounter()
            elif self.buttons['Stop'].collidepoint(pos):
                self.simulation.stopCounter()
            elif self.buttons['Reset'].collidepoint(pos):
                self.simulation.resetCounter()
