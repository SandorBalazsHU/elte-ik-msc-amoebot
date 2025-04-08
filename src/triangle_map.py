import pygame
import math

from src.config import Config
from src.drawer import AntiAliasedDrawer

'''
NE FELEDD:
    0 = bal-fel
    1 = jobb-fel
    2 = bal
    3 = jobb
    4 = bal-le
    5 = jobb-le
'''
class TriangleMap:
    def __init__(self):
        self.triangle_grid = []
        self.occupied = []
        self.__generate_triangle_grid()
        self.clear_occupied()

    def clear_occupied(self):
        self.occupied = [[False for _ in range(Config.Grid.COLS)] for _ in range(Config.Grid.ROWS)]

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
    
    def get_target_position(self, row, col, heading):
        directions = self.get_neighbor_directions(row)
        if heading is None or heading < 0 or heading >= len(directions):
            return None
        dr, dc = directions[heading]
        target_row = row + dr
        target_col = col + dc
        if self.is_valid(target_row, target_col):
            return (target_row, target_col)
        return None

    def is_valid(self, row, col):
        return 0 <= row < Config.Grid.ROWS and 0 <= col < Config.Grid.COLS
    
    def get_valid_target_position(self, row, col, heading):
        target = self.get_target_position(row, col, heading)
        if target and not self.is_occupied(*target):
            return target
        return None

    def get_heading_from_direction(self, from_row, from_col, to_row, to_col):
        directions = self.get_neighbor_directions(from_row)
        dr = to_row - from_row
        dc = to_col - from_col
        for index, (d_row, d_col) in enumerate(directions):
            if dr == d_row and dc == d_col:
                return index
        return None  # Nem szomszédos pont