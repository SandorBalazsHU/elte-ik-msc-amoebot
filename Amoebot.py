import pygame
import sys
import math
import random

# Beállítások
WIDTH, HEIGHT = 800, 600
BACKGROUND_COLOR = (30, 30, 30)
GRID_COLOR = (80, 80, 80)
NODE_COLOR = (180, 180, 180)
NODE_RADIUS = 5
EDGE_WIDTH = 1
FPS = 30

# Háromszögrács létrehozása
GRID_ROWS = 10
GRID_COLS = 10
NODE_DISTANCE = 50

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

# Háromszögrács generálása
def generate_triangle_grid():
    grid = []
    for row in range(GRID_ROWS):
        row_points = []
        for col in range(GRID_COLS):
            x = col * NODE_DISTANCE + (NODE_DISTANCE // 2 if row % 2 else 0)
            y = row * NODE_DISTANCE * math.sin(math.radians(60))
            row_points.append((x + 100, int(y) + 100))
        grid.append(row_points)
    return grid

grid_points = generate_triangle_grid()

# Szomszédok meghatározása
def get_neighbors(row, col):
    directions_even = [(-1, -1), (-1, 0), (0, -1), (0, 1), (1, -1), (1, 0)]
    directions_odd = [(-1, 0), (-1, 1), (0, -1), (0, 1), (1, 0), (1, 1)]
    directions = directions_odd if row % 2 else directions_even
    neighbors = []
    for dr, dc in directions:
        nr, nc = row + dr, col + dc
        if 0 <= nr < GRID_ROWS and 0 <= nc < GRID_COLS:
            neighbors.append((nr, nc))
    return neighbors

# Amoebot osztály
class Amoebot:
    def __init__(self, row, col):
        self.row = row
        self.col = col
        self.from_pos = (row, col)
        self.to_pos = (row, col)
        self.color = [random.randint(50, 255) for _ in range(3)]
        self.phase = "idle"  # idle, phase1, phase2
        self.progress = 0.0
        self.speed = 0.02

    def update(self):
        if self.phase == "idle":
            neighbors = get_neighbors(self.row, self.col)
            if neighbors:
                target = random.choice(neighbors)
                self.from_pos = (self.row, self.col)
                self.to_pos = target
                self.phase = "phase1"
                self.progress = 0.0

        elif self.phase == "phase1":
            self.progress += self.speed
            if self.progress >= 1.0:
                self.progress = 0.0
                self.phase = "phase2"

        elif self.phase == "phase2":
            self.progress += self.speed
            if self.progress >= 1.0:
                self.row, self.col = self.to_pos
                self.phase = "idle"
                self.progress = 0.0

    def draw(self, surface):
        p1 = grid_points[self.from_pos[0]][self.from_pos[1]]
        p2 = grid_points[self.to_pos[0]][self.to_pos[1]]

        if self.phase == "idle":
            pygame.draw.circle(surface, self.color, p1, 10)
        else:
            if self.phase == "phase1":
                f1 = (p1[0] + (p2[0] - p1[0]) * self.progress,
                      p1[1] + (p2[1] - p1[1]) * self.progress)
                f2 = p2
            elif self.phase == "phase2":
                f1 = p2
                f2 = (p1[0] + (p2[0] - p1[0]) * (1 - self.progress),
                      p1[1] + (p2[1] - p1[1]) * (1 - self.progress))
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

# Amoebotok színtér katalógus
amoebots = [Amoebot(random.randint(0, GRID_ROWS - 1), random.randint(0, GRID_COLS - 1)) for _ in range(5)]

# Fő szimulációs loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    screen.fill(BACKGROUND_COLOR)

    # Rács kirajzolása
    for r, row in enumerate(grid_points):
        for c, p in enumerate(row):
            pygame.draw.circle(screen, NODE_COLOR, p, NODE_RADIUS)
            for nr, nc in get_neighbors(r, c):
                neighbor = grid_points[nr][nc]
                pygame.draw.line(screen, GRID_COLOR, p, neighbor, EDGE_WIDTH)

    # Amoebotok frissítése és kirajzolása
    for amoebot in amoebots:
        amoebot.update()
        amoebot.draw(screen)

    pygame.display.flip()
    clock.tick(FPS)
