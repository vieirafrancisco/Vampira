import math

import pygame

from settings import *
from utils.functions import get_two_nodes_distance

class Player(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        self._layer = PLAYER_LAYER
        self.groups = (game.sprites)
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pygame.Surface((PLAYER_WIDTH, PLAYER_HEIGHT))
        self.image.fill(WHITE)
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
            if self.game.map_array[x][y] not in NOT_NODES:
                d = self.game.dists[(x, y)]
                if 0 < d <= self.walk_range:
                    self.rect.topleft = (x * PLAYER_WIDTH, y * PLAYER_HEIGHT)
                    self.pos = (x, y)
                    self.game.make_graph()