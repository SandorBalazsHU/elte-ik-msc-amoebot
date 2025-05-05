import pygame
import pygame_menu
class Config:
    class Window:
        WIDTH = 800
        HEIGHT = 600
        FPS = 30
        CAPTION = "Amoebot simulator 🦠 v0.8"
        ICON_PATH = "src/assets/icon.png"
        BACKGROUND_COLOR = (30, 30, 30)

    class Grid:
        ROWS = 15
        COLS = 15
        NODE_DISTANCE = 50
        PADDING = 50
        NODE_COLOR = (180, 180, 180)
        GRID_COLOR = (80, 80, 80)
        NODE_RADIUS = 5
        EDGE_WIDTH = 1

    class Amoebot:
        CIRCLE_SIZE = 10
        EYE_COLOR = (255, 255, 255)
        EYE_SIZE = 2
        IDLE_DELAY = 15
        SPEED = 0.02
        DEFAULT_HEADING = 3
    
    class Scene:
        WHITE = (255, 255, 255)
        GRAY = (30, 30, 30)
        SRED = (255, 100, 100)
        GREEN = (100, 255, 100)
        BLACK = (0, 0, 0)
        FONT1_SIZE = 30
        FONT2_SIZE = 15
        DEFAULT_BUTTON_COLOR = (220, 220, 220)
        DEFAULT_BUTTON_TEXT_COLOR = (0, 0, 0)
        DEFAULT_TEXT_COLOR = (255, 255, 255)
        BOT_NUMBER = 30
        show_grid = True
        jump_pos = True