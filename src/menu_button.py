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