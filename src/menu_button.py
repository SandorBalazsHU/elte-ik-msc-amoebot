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
    LABEL_OFFSET_Y = 8           # lefelé tolás a szövegeken
    BUTTON_SPACING_X = 10        # gombok közti vízszintes távolság
    ELEMENT_SPACING_X = 85       # a "Step counter" és az első gomb közti távolság

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

        # Gombok pozíciójának kiszámítása
        button_width = 60
        button_height = 30
        start_x = self.x + self.ELEMENT_SPACING_X

        self.buttons = {
            'Start': pygame.Rect(start_x, self.y, button_width, button_height),
            'Stop': pygame.Rect(start_x + (button_width + self.BUTTON_SPACING_X), self.y, button_width, button_height),
            'Reset': pygame.Rect(start_x + 2 * (button_width + self.BUTTON_SPACING_X), self.y, button_width, button_height)
        }

    def setSimulation(self, simulation):
        self.simulation = simulation

    def draw(self, surface):
        # Lépésszámláló címke
        label = self.font.render("Step counter", True, self.label_color)
        surface.blit(label, (self.x, self.y + self.LABEL_OFFSET_Y))

        # Gombok színei állapot szerint
        for name, rect in self.buttons.items():
            if name == 'Start' and self.simulation and self.simulation.step_counter_running:
                color = (0, 200, 0)
            elif name == 'Stop' and self.simulation and not self.simulation.step_counter_running:
                color = (200, 0, 0)
            else:
                color = self.color

            pygame.draw.rect(surface, color, rect, border_radius=5)
            text_surf = self.font.render(name, True, self.text_color)
            text_rect = text_surf.get_rect(center=rect.center)
            surface.blit(text_surf, text_rect)

        # Lépésszám érték kirajzolása
        if self.simulation:
            steps_label = self.font.render(f"Steps: {self.simulation.step_counter}", True, self.label_color)
            step_x = self.buttons['Reset'].right + self.BUTTON_SPACING_X
            surface.blit(steps_label, (step_x, self.y + self.LABEL_OFFSET_Y))

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
