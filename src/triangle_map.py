import pygame
import math

from src.config import Config
from src.drawer import AntiAliasedDrawer

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
        size = (0,0)
        size_x = (self.PADDING*2) + (self.row*self.node_distance) - (self.node_distance/2)
        size_y = (self.PADDING) + (self.col*self.node_distance) - (self.node_distance*2)
        size = (size_x,size_y)
        return size

    def __generate_triangle_grid(self):
        for row in range(self.row):
            row_points = []
            for col in range(self.col):
                x = col * self.node_distance + (self.node_distance // 2 if row % 2 else 0)
                y = row * self.node_distance * math.sin(math.radians(60))
                row_points.append((x + self.PADDING, int(y) + self.PADDING))
            self.triangle_grid.append(row_points)

    def create_grid_surface(self, triangle_grid, get_neighbors, node_color, grid_color, node_radius, edge_width, width, height):
        surface = pygame.Surface((width, height), pygame.SRCALPHA)
        drawer = AntiAliasedDrawer(surface)
        for r, row in enumerate(triangle_grid):
            for c, point in enumerate(row):
                drawer.draw_circle(node_color, point, node_radius)
                for nr, nc in get_neighbors(r, c):
                    neighbor = triangle_grid[nr][nc]
                    drawer.draw_line(grid_color, point, neighbor, edge_width)
        return surface

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