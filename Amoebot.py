import pygame
import sys
import math
import random

class Simulation:
    def __init__(self):
        self.WIDTH, self.HEIGHT = 800, 600
        self.BACKGROUND_COLOR = (30, 30, 30)
        self.GRID_COLOR = (80, 80, 80)
        self.NODE_COLOR = (180, 180, 180)
        self.NODE_RADIUS = 5
        self.EDGE_WIDTH = 1
        self.FPS = 30
        self.GRID_ROWS = 15
        self.GRID_COLS = 15
        self.NODE_DISTANCE = 50
        self.RANDOM_START = False
        self.BOT_NUMBER = 12
        self.screan = 0
        self.clock = 0
        self.triangle_map = []
        self.amoebots = []
        self.init()

    def init(self):
        pygame.init()
        self.triangle_map = TriangleMap(self.GRID_ROWS,self.GRID_COLS, self.NODE_DISTANCE)
        size = self.triangle_map.get_window_size()
        self.WIDTH = size[0]
        self.HEIGHT = size[1]
        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        self.clock = pygame.time.Clock()
        if self.RANDOM_START:
            self.amoebots = [Amoebot(self.triangle_map, random.randint(0, self.GRID_ROWS - 1), random.randint(0, self.GRID_COLS - 1)) for _ in range(self.BOT_NUMBER)]
        else:
            for i in range(1,self.BOT_NUMBER + 1):
                self.amoebots.append(Amoebot(self.triangle_map, i, 1))

    
    def _draw_triangle_grid(self):
        for r, row in enumerate(self.triangle_map.triangle_grid):
            for c, p in enumerate(row):
                pygame.draw.circle(self.screen, self.NODE_COLOR, p, self.NODE_RADIUS)
                for nr, nc in self.triangle_map.get_neighbors(r, c):
                    neighbor = self.triangle_map.triangle_grid[nr][nc]
                    pygame.draw.line(self.screen, self.GRID_COLOR, p, neighbor, self.EDGE_WIDTH)

    def start(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            self.screen.fill(self.BACKGROUND_COLOR)
            self._draw_triangle_grid()
            for amoebot in self.amoebots:
                amoebot.update()
                amoebot.draw(self.screen)

            pygame.display.flip()
            self.clock.tick(self.FPS)
class TriangleMap:
    def __init__(self, row:int, col:int, node_distance: int):
        self.PADDING = 50
        self.row = row
        self.col = col
        self.node_distance = node_distance
        self.triangle_grid = []
        self.__generate_triangle_grid()

    def get_window_size(self):
        size = [0,0]
        size_x = (self.PADDING*2) + (self.row*self.node_distance) - (self.node_distance/2)
        size_y = (self.PADDING) + (self.col*self.node_distance) - (self.node_distance*2)
        size = [size_x,size_y]
        return size

    def __generate_triangle_grid(self):
        for row in range(self.row):
            row_points = []
            for col in range(self.col):
                x = col * self.node_distance + (self.node_distance // 2 if row % 2 else 0)
                y = row * self.node_distance * math.sin(math.radians(60))
                row_points.append((x + self.PADDING, int(y) + self.PADDING))
            self.triangle_grid.append(row_points)

    def get_neighbors(self, row, col):
        triangle_neighbors = []
        directions_even = [(-1, -1), (-1, 0), (0, -1), (0, 1), (1, -1), (1, 0)]
        directions_odd = [(-1, 0), (-1, 1), (0, -1), (0, 1), (1, 0), (1, 1)]
        directions = directions_odd if row % 2 else directions_even
        for dr, dc in directions:
            nr, nc = row + dr, col + dc
            if 0 <= nr < self.row and 0 <= nc < self.col:
                triangle_neighbors.append((nr, nc))
        return triangle_neighbors
    
class Amoebot():
    def __init__(self, triangle_map:TriangleMap,  row: int, col:int):
        self.triangle_map = triangle_map
        self.row = row
        self.col = col
        self.from_pos = (self.row, self.col)
        self.to_pos = (self.row, self.col)
        self.color = [random.randint(50, 255) for _ in range(3)]
        self.phase = "idle"
        self.progress = 0.0
        self.speed = 0.02
        self.idle_timer = 0
        self.idle_delay = 15
        self.target = (0,0)
        self.heading = 3

    def update(self):
        if self.phase == "idle":
            self.idle_timer += 1
            if self.idle_timer >= self.idle_delay:
                neighbors = self.triangle_map.get_neighbors(self.row, self.col)
                if neighbors:
                    #target = random.choice(neighbors)
                    target = neighbors[self.heading]
                    self.from_pos = (self.row, self.col)
                    self.to_pos = target
                    self.phase = "phase1"
                    self.progress = 0.0
                    self.idle_timer = 0

        elif self.phase == "phase1":
            self.progress += self.speed
            if self.progress >= 1.0:
                self.progress = 0.0
                self.phase = "phase2"

        elif self.phase == "phase2":
            self.progress += self.speed
            if self.progress >= 1.0:
                self.row, self.col = self.to_pos
                self.from_pos = self.to_pos
                self.phase = "idle"
                self.progress = 0.0
                self.idle_timer = 0

    def draw(self, surface):
        p1 = self.triangle_map.triangle_grid[self.from_pos[0]][self.from_pos[1]]
        p2 = self.triangle_map.triangle_grid[self.to_pos[0]][self.to_pos[1]]

        if self.phase == "idle":
            pygame.draw.circle(surface, self.color, p1, 10)
        else:
            if self.phase == "phase1":
                f1 = (p1[0] + (p2[0] - p1[0]) * self.progress,
                      p1[1] + (p2[1] - p1[1]) * self.progress)
                f2 = p1
            elif self.phase == "phase2":
                f1 = p2
                f2 = (p1[0] + (p2[0] - p1[0]) * self.progress,
                    p1[1] + (p2[1] - p1[1]) * self.progress)
            else:
                f1 = f2 = p1

            dx = f2[0] - f1[0]
            dy = f2[1] - f1[1]
            length = math.hypot(dx, dy)
            angle = math.atan2(dy, dx)
            ellipse_rect = pygame.Rect(0, 0, length, 20)
            ellipse_rect.center = ((f1[0] + f2[0]) // 2, (f1[1] + f2[1]) // 2)
            rotated_surf = pygame.Surface((length, 20), pygame.SRCALPHA)
            pygame.draw.ellipse(rotated_surf, self.color, rotated_surf.get_rect())
            rotated_surf = pygame.transform.rotate(rotated_surf, -math.degrees(angle))
            rotated_rect = rotated_surf.get_rect(center=ellipse_rect.center)
            surface.blit(rotated_surf, rotated_rect)

def main():
    simulation = Simulation()
    simulation.start()

if __name__ == "__main__":
    main()