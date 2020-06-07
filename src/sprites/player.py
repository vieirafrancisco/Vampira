import math

import pygame

from settings import *
from utils.functions import get_two_nodes_distance

def inside_canvas(x, y):
    if x * TILE_SIZE < CANVAS_WIDTH and y * TILE_SIZE < CANVAS_HEIGHT:
        return True
    else:
        return False

class Player(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        self._layer = PLAYER_LAYER
        self.groups = (game.sprites)
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pygame.Surface((PLAYER_WIDTH, PLAYER_HEIGHT)).convert()
        self.image.blit(self.game.player_image, (0, 0), (1 * PLAYER_WIDTH, 0 * PLAYER_HEIGHT, PLAYER_WIDTH, PLAYER_HEIGHT))
        self.image.set_colorkey(COLOR_KEY)
        self.rect = self.image.get_rect()
        self.rect.topleft = (x * PLAYER_WIDTH, y * PLAYER_HEIGHT)
        self.pos = (x, y)
        self.walk_range = PLAYER_WALK_RANGE

    def update(self):
        mouse_click = pygame.mouse.get_pressed()[0]
        if mouse_click:
            mouse_pos = pygame.mouse.get_pos()
            x = math.floor(mouse_pos[0] / TILE_SIZE)
            y = math.floor(mouse_pos[1] / TILE_SIZE)
            if inside_canvas(x, y) and self.game.map_array[x][y] not in NOT_NODES:
                d = self.game.dists[(x, y)]
                if 0 < d <= self.walk_range:
                    self.rect.topleft = (x * PLAYER_WIDTH, y * PLAYER_HEIGHT)
                    self.pos = (x, y)
                    self.game.make_graph()