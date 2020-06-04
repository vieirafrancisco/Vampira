import math

import pygame

# game
TILE_SIZE = 32
FPS = 60
vec = pygame.Vector2
INF = math.inf

# window
WIDTH = TILE_SIZE * 9
HEIGHT = TILE_SIZE * 15

# colors
BLACK = (0, 0 ,0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
GRAY = (120, 120, 120)
BROWN = (180, 120, 80)
COLOR_LIST = [BLACK, WHITE, RED, GREEN, BLUE, GRAY, BROWN]

# player
PLAYER_WIDTH = 32
PLAYER_HEIGHT = 32