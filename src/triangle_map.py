import pygame
import math

from src.config import Config
from src.drawer import AntiAliasedDrawer

class TriangleMap:
    def __init__(self):
        self.triangle_grid = []
        self.occupied = [[False for _ in range(Config.Grid.COLS)] for _ in range(Config.Grid.ROWS)]
        self.__generate_triangle_grid()

    def is_occupied(self, row, col):
        return self.occupied[row][col]

    def occupy(self, row, col):
        self.occupied[row][col] = True

    def release(self, row, col):
        self.occupied[row][col] = False

    def get_window_size(self):
        size = (0,0)
        size_x = (Config.Grid.PADDING*2) + (Config.Grid.ROWS*Config.Grid.NODE_DISTANCE) - (Config.Grid.NODE_DISTANCE/2)
        size_y = (Config.Grid.PADDING) + (Config.Grid.COLS*Config.Grid.NODE_DISTANCE) - (Config.Grid.NODE_DISTANCE*2)
        size = (size_x,size_y)
        return size

    def __generate_triangle_grid(self):
        for row in range(Config.Grid.ROWS):
            row_points = []
            for col in range(Config.Grid.COLS):
                x = col * Config.Grid.NODE_DISTANCE + (Config.Grid.NODE_DISTANCE // 2 if row % 2 else 0)
                y = row * Config.Grid.NODE_DISTANCE * math.sin(math.radians(60))
                row_points.append((x + Config.Grid.PADDING, int(y) + Config.Grid.PADDING))
            self.triangle_grid.append(row_points)

    def create_grid_surface(self, width, height):
        surface = pygame.Surface((width, height), pygame.SRCALPHA)
        drawer = AntiAliasedDrawer(surface)
        for r, row in enumerate(self.triangle_grid):
            for c, point in enumerate(row):
                drawer.draw_circle(Config.Grid.NODE_COLOR, point, Config.Grid.NODE_RADIUS)
                for nr, nc in self.get_neighbors(r, c):
                    neighbor = self.triangle_grid[nr][nc]
                    drawer.draw_line(Config.Grid.GRID_COLOR, point, neighbor, Config.Grid.EDGE_WIDTH)
        return surface

    def get_neighbors(self, row, col):
        triangle_neighbors = []
        directions_even = [(-1, -1), (-1, 0), (0, -1), (0, 1), (1, -1), (1, 0)]
        directions_odd = [(-1, 0), (-1, 1), (0, -1), (0, 1), (1, 0), (1, 1)]
        directions = directions_odd if row % 2 else directions_even
        for dr, dc in directions:
            nr, nc = row + dr, col + dc
            if 0 <= nr < Config.Grid.ROWS and 0 <= nc < Config.Grid.COLS:
                triangle_neighbors.append((nr, nc))
        return triangle_neighbors

    def get_neighbor_directions(self, row):
        directions_even = [(-1, -1), (-1, 0), (0, -1), (0, 1), (1, -1), (1, 0)]
        directions_odd  = [(-1, 0), (-1, 1), (0, -1), (0, 1), (1, 0), (1, 1)]
        return directions_odd if row % 2 else directions_even

    def is_valid(self, row, col):
        return 0 <= row < Config.Grid.ROWS and 0 <= col < Config.Grid.COLS