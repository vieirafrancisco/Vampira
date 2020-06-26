import os
import math

import pygame

# game
TILE_SIZE = 32
FPS = 60
vec = pygame.Vector2
INF = math.inf
DIRECTIONS = [(0, 1), (0, -1), (1, 0), (-1, 0)]

# window
WIDTH = TILE_SIZE * 9
HEIGHT = TILE_SIZE * 16
CANVAS_WIDTH = WIDTH
CANVAS_HEIGHT = HEIGHT - TILE_SIZE

# paths
RESOURCE_PATHS = {
    "spritesheets": os.path.join("resources", "spritesheets"),
    "maps": os.path.join("resources", "maps")
}

# colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
DARK_RED = (75, 0, 0)
GREEN = (0, 255, 0)
DARK_GREEN = (0, 120, 0)
BLUE = (0, 0, 255)
LITE_DARK_BLUE = (0, 0, 75)
DARK_BLUE = (38, 36, 49)
GRAY = (120, 120, 120)
DARK_GRAY = (25, 25, 25)
BROWN = (180, 120, 80)
DARK_BROWN = (90, 50, 10)
COLOR_KEY = (240, 0, 222)
COLOR_LIST = [BLACK, WHITE, RED, GREEN, BLUE, GRAY, BROWN, DARK_GRAY, DARK_BROWN]

# player
PLAYER_WIDTH = 32
PLAYER_HEIGHT = 32
PLAYER_WALK_RANGE = 3
PLAYER_SPEED = 2

# mob
MOB_SPEED = 2
MOB_VISION_RANGE = 3

# layers
PLAYER_LAYER = 2
WALL_LAYER = 1
ITEM_LAYER = 1

# indentifiers
EMPTY = 0
PLAYER = 1
WALL = 2
GROUND = 3
MOB = 4
STAIRS = 5
NOT_NODES = [WALL]

# map
MAPS_FOLDER_PATH = os.path.join("resources", "maps", "blueprints")
