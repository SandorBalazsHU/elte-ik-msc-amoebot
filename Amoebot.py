import pygame
import sys
import math
import random

# Beállítások
WIDTH, HEIGHT = 800, 600
BACKGROUND_COLOR = (30, 30, 30)
GRID_COLOR = (80, 80, 80)
NODE_COLOR = (180, 180, 180)
AMOEBOT_COLOR = (0, 255, 0)
NODE_RADIUS = 5
EDGE_WIDTH = 1
ELLIPSE_WIDTH = 3
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
        self.target = None
        self.expanding = True

    def update(self):
        if self.target is None and self.expanding:
            neighbors = get_neighbors(self.row, self.col)
            if neighbors:
                self.target = random.choice(neighbors)
        elif not self.expanding:
            self.row, self.col = self.target
            self.target = None
        self.expanding = not self.expanding

    def draw(self, surface):
        p1 = grid_points[self.row][self.col]
        if self.target:
            p2 = grid_points[self.target[0]][self.target[1]]
            center = ((p1[0]+p2[0])//2, (p1[1]+p2[1])//2)
            dx = p2[0] - p1[0]
            dy = p2[1] - p1[1]
            angle = math.atan2(dy, dx)
            length = math.hypot(dx, dy)
            ellipse_rect = pygame.Rect(0, 0, length, 20)
            ellipse_rect.center = center
            rotated_surf = pygame.Surface((length, 20), pygame.SRCALPHA)
            pygame.draw.ellipse(rotated_surf, AMOEBOT_COLOR, rotated_surf.get_rect(), ELLIPSE_WIDTH)
            rotated_surf = pygame.transform.rotate(rotated_surf, -math.degrees(angle))
            rotated_rect = rotated_surf.get_rect(center=center)
            surface.blit(rotated_surf, rotated_rect)
        else:
            pygame.draw.circle(surface, AMOEBOT_COLOR, p1, 10)

# Amoebotok színtér katalógus
amoebots = [Amoebot(random.randint(0, GRID_ROWS-1), random.randint(0, GRID_COLS-1)) for _ in range(5)]

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