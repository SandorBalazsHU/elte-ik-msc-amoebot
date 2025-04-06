import pygame
import pygame.gfxdraw
import math

class AntiAliasedDrawer:
    def __init__(self, surface):
        self.surface = surface

    def draw_circle(self, color, pos, radius):
        x, y = int(pos[0]), int(pos[1])
        pygame.gfxdraw.aacircle(self.surface, x, y, radius, color)
        pygame.gfxdraw.filled_circle(self.surface, x, y, radius, color)

    def draw_line(self, color, start_pos, end_pos, width=1):
        if width == 1:
            pygame.draw.aaline(self.surface, color, start_pos, end_pos)
        else:
            pygame.draw.line(self.surface, color, start_pos, end_pos, width)

    def draw_ellipse(self, f1, f2, color):
        dx = f2[0] - f1[0]
        dy = f2[1] - f1[1]
        length = math.hypot(dx, dy)
        angle = math.atan2(dy, dx)
        center = ((f1[0] + f2[0]) / 2, (f1[1] + f2[1]) / 2)
        upscale = 6 
        big_width = int(length * upscale)
        big_height = 20 * upscale
        big_surf = pygame.Surface((big_width, big_height), pygame.SRCALPHA)
        pygame.draw.ellipse(big_surf, color, big_surf.get_rect())
        small_surf = pygame.transform.smoothscale(big_surf, (int(length), 20))
        rotated_surf = pygame.transform.rotozoom(small_surf, -math.degrees(angle), 1.0)
        rotated_rect = rotated_surf.get_rect(center=center)
        self.surface.blit(rotated_surf, rotated_rect)