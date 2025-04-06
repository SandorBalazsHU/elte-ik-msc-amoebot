import random
import math

from src.config import Config
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from src.triangle_map import TriangleMap

class Amoebot():
    def __init__(self, triangle_map: 'TriangleMap',  row: int, col:int):
        self.triangle_map = triangle_map
        self.row = row
        self.col = col
        self.CIRCLE_SIZE = 10
        self.from_pos = (self.row, self.col)
        self.to_pos = (self.row, self.col)
        self.color = [random.randint(50, 255) for _ in range(3)]
        self.EYE_COLOR = (255, 255, 255)
        self.EYE_SIZE = 2
        self.EYE_ON = True
        self.phase = "idle"
        self.progress = 0.0
        self.speed = 0.02
        self.idle_timer = 0
        self.idle_delay = 15
        self.target = (0,0)
        self.heading = 3
        self.RANDOM_HEADING = True

    def _target_select(self):
        neighbors = self.triangle_map.get_neighbors(self.row, self.col)
        free_neighbors = [n for n in neighbors if not self.triangle_map.is_occupied(*n)]
        if not free_neighbors:
            return False  # nincs hova menni
        if self.RANDOM_HEADING:
            self.target = random.choice(free_neighbors)
        else:
            self.target = neighbors[self.heading]
        return True

    def update(self):
        if self.phase == "idle":
            self.update_idle()
        elif self.phase == "expansion":
            self.update_expansion()
        elif self.phase == "contraction":
            self.update_contraction()

    def update_idle(self):
        if self.heading != -1:
            self.idle_timer += 1
            if self.idle_timer >= self.idle_delay:
                if self._target_select():
                    self.from_pos = (self.row, self.col)
                    self.to_pos = self.target
                    self.triangle_map.occupy(*self.to_pos)  # előre lefoglaljuk
                    self.triangle_map.release(*self.from_pos)
                    self.phase = "expansion"
                    self.progress = 0.0
                    self.idle_timer = 0
    
    def update_expansion(self):
        self.progress += self.speed
        if self.progress >= 1.0:
            self.progress = 0.0
            self.phase = "contraction"

            p1 = self.triangle_map.triangle_grid[self.from_pos[0]][self.from_pos[1]]
            p2 = self.triangle_map.triangle_grid[self.to_pos[0]][self.to_pos[1]]

            dist = math.dist(p1, p2)
            offset = self.CIRCLE_SIZE / dist
            t = 1.0 * (1 + offset)

            self.contraction_f1 = (
                p1[0] + (p2[0] - p1[0]) * t,
                p1[1] + (p2[1] - p1[1]) * t
            )

    def update_contraction(self):
        self.progress += self.speed
        if self.progress >= 1.0:
            self.row, self.col = self.to_pos
            self.from_pos = self.to_pos
            self.phase = "idle"
            self.progress = 0.0
            self.idle_timer = 0


    def draw(self, drawer):
        p1 = self.triangle_map.triangle_grid[self.from_pos[0]][self.from_pos[1]]
        p2 = self.triangle_map.triangle_grid[self.to_pos[0]][self.to_pos[1]]

        if self.phase == "idle":
            self.draw_idle(p2, drawer)
        elif self.phase == "expansion":
            self.draw_expansion(p1, p2, drawer)
        elif self.phase == "contraction":
            self.draw_contraction(p1, p2, drawer)
        else:
            drawer.draw_circle(self.color, p1, self.CIRCLE_SIZE)

    def draw_idle(self, pos, drawer):
        drawer.draw_circle(self.color, pos, self.CIRCLE_SIZE)
        if self.EYE_ON:
            self.draw_eye(pos, pos, drawer)

    def draw_expansion(self, p1, p2, drawer):
        dx = p2[0] - p1[0]
        dy = p2[1] - p1[1]
        dist = math.hypot(dx, dy)
        offset = self.CIRCLE_SIZE / dist

        f1_start = (p1[0] + dx * offset, p1[1] + dy * offset)
        f1_end = (p1[0] + dx * (1 + offset), p1[1] + dy * (1 + offset))
        f1 = (
            f1_start[0] + (f1_end[0] - f1_start[0]) * self.progress,
            f1_start[1] + (f1_end[1] - f1_start[1]) * self.progress
        )
        f2 = (p1[0] - dx * offset, p1[1] - dy * offset)
        self.contraction_f1 = f1_end

        drawer.draw_ellipse(f1, f2, self.color)
        if self.EYE_ON:
            self.draw_eye(f1, f2, drawer)

    def draw_contraction(self, p1, p2, drawer):
        dist = math.dist(p1, p2)
        offset = self.CIRCLE_SIZE / dist
        f1 = self.contraction_f1
        t = self.progress * (1 - offset)
        f2 = (
            p1[0] + (p2[0] - p1[0]) * t,
            p1[1] + (p2[1] - p1[1]) * t
        )

        drawer.draw_ellipse(f1, f2, self.color)
        if self.EYE_ON:
            self.draw_eye(f1, f2, drawer)

    def draw_eye(self, f1, f2, drawer):
        eye_x = f1[0] + (f2[0] - f1[0]) * 0.1
        eye_y = f1[1] + (f2[1] - f1[1]) * 0.1
        drawer.draw_circle(self.EYE_COLOR, (eye_x, eye_y), self.EYE_SIZE)