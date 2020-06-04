import math

import pygame

from settings import *

class Player(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        self._layer = 2
        self.groups = (game.sprites)
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.image = pygame.Surface((PLAYER_WIDTH, PLAYER_HEIGHT))
        self.image.fill(WHITE)
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)

    def update(self):
        mouse_click = pygame.mouse.get_pressed()[0]
        if mouse_click:
            mouse_pos = pygame.mouse.get_pos()
            x = math.floor(mouse_pos[0] / TILE_SIZE)
            y = math.floor(mouse_pos[1] / TILE_SIZE)
            self.rect.topleft = (x * TILE_SIZE, y * TILE_SIZE)