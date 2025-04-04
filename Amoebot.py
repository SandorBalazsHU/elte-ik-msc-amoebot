import pygame
import pygame.gfxdraw
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
        self.RANDOM_START = True
        self.BOT_NUMBER = 12
        self.screan = 0
        self.clock = 0
        self.triangle_map = []
        self.amoebots = []
        self.init()
        self.drawer: AntiAliasedDrawer

    def init(self):
        pygame.init()
        self.triangle_map = TriangleMap(self.GRID_ROWS,self.GRID_COLS, self.NODE_DISTANCE)
        size = self.triangle_map.get_window_size()
        self.WIDTH = size[0]
        self.HEIGHT = size[1]
        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        self.drawer = AntiAliasedDrawer(self.screen)
        self.clock = pygame.time.Clock()
        if self.RANDOM_START:
            self.amoebots = [Amoebot(self.triangle_map, random.randint(0, self.GRID_ROWS - 1),
                                      random.randint(0, self.GRID_COLS - 1)) for _ in range(self.BOT_NUMBER)]
        else:
            for i in range(1,self.BOT_NUMBER + 1):
                self.amoebots.append(Amoebot(self.triangle_map, i, 1))
    
    def _draw_triangle_grid(self):
        for r, row in enumerate(self.triangle_map.triangle_grid):
            for c, point in enumerate(row):
                self.drawer.draw_circle(self.NODE_COLOR, point, self.NODE_RADIUS)
                for nr, nc in self.triangle_map.get_neighbors(r, c):
                    neighbor = self.triangle_map.triangle_grid[nr][nc]
                    self.drawer.draw_line(self.GRID_COLOR, point, neighbor, self.EDGE_WIDTH)

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
                amoebot.draw(self.drawer)
            pygame.display.flip()
            self.clock.tick(self.FPS)
class TriangleMap:
    def __init__(self, row:int, col:int, node_distance: int):
        self.PADDING = 50
        self.row = row
        self.col = col
        self.node_distance = node_distance
        self.triangle_grid = []
        self.occupied = [[False for _ in range(col)] for _ in range(row)]
        self.__generate_triangle_grid()

    def is_occupied(self, row, col):
        return self.occupied[row][col]

    def occupy(self, row, col):
        self.occupied[row][col] = True

    def release(self, row, col):
        self.occupied[row][col] = False

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
            # ha az eredeti irány foglalt, próbál mást
            if self.triangle_map.is_occupied(*neighbors[self.heading]):
                self.target = random.choice(free_neighbors)
            else:
                self.target = neighbors[self.heading]
        return True

    def update(self):
        if self.phase == "idle":
            self.idle_timer += 1
            if self.idle_timer >= self.idle_delay:
                self._target_select()
                self.from_pos = (self.row, self.col)
                self.to_pos = self.target
                self.triangle_map.occupy(*self.to_pos)  # előre lefoglaljuk
                self.phase = "phase1"
                self.progress = 0.0
                self.idle_timer = 0

        elif self.phase == "phase1":
            self.progress += self.speed
            if self.progress >= 1.0:
                self.progress = 0.0
                self.phase = "phase2"
                p1 = self.triangle_map.triangle_grid[self.from_pos[0]][self.from_pos[1]]
                p2 = self.triangle_map.triangle_grid[self.to_pos[0]][self.to_pos[1]]
                dist = math.dist(p1, p2)
                offset = self.CIRCLE_SIZE / dist
                t = 1.0 * (1 + offset)
                self.phase2_f1 = (p1[0] + (p2[0] - p1[0]) * t,
                                  p1[1] + (p2[1] - p1[1]) * t)
                
        elif self.phase == "phase2":
            self.progress += self.speed
            if self.progress >= 1.0:
                self.triangle_map.release(*self.from_pos)
                self.row, self.col = self.to_pos
                self.from_pos = self.to_pos
                self.phase = "idle"
                self.progress = 0.0
                self.idle_timer = 0

    def draw(self, drawer):
        p1 = self.triangle_map.triangle_grid[self.from_pos[0]][self.from_pos[1]]
        p2 = self.triangle_map.triangle_grid[self.to_pos[0]][self.to_pos[1]]
        if self.phase == "idle":
            drawer.draw_circle(self.color, p2, self.CIRCLE_SIZE)
            if self.EYE_ON:
                drawer.draw_circle(self.EYE_COLOR, p2, self.EYE_SIZE)
        else:
            dist = math.dist(p1, p2)
            offset = self.CIRCLE_SIZE / dist
            if self.phase == "phase1":
                dx = p2[0] - p1[0]
                dy = p2[1] - p1[1]
                dist = math.hypot(dx, dy)
                offset = self.CIRCLE_SIZE / dist
                f1_start = (p1[0] + dx * offset,
                            p1[1] + dy * offset)
                f1_end = (p1[0] + dx * (1 + offset),
                          p1[1] + dy * (1 + offset))
                f1 = (f1_start[0] + (f1_end[0] - f1_start[0]) * self.progress,
                      f1_start[1] + (f1_end[1] - f1_start[1]) * self.progress)
                f2 = (p1[0] - dx * offset, 
                      p1[1] - dy * offset)
                self.phase2_f1 = f1_end
            elif self.phase == "phase2":
                f1 = self.phase2_f1
                t = self.progress * (1 - offset)
                f2 = (p1[0] + (p2[0] - p1[0]) * t,
                    p1[1] + (p2[1] - p1[1]) * t)
            else:
                f1 = f2 = p1
            drawer.draw_ellipse(f1, f2, self.color)
            if self.EYE_ON:
                eye_x = f1[0] + (f2[0] - f1[0]) * 0.1
                eye_y = f1[1] + (f2[1] - f1[1]) * 0.1
                drawer.draw_circle((255, 255, 255), (eye_x, eye_y), 2)
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

def main():
    simulation = Simulation()
    simulation.start()

if __name__ == "__main__":
    main()