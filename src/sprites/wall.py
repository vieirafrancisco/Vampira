import pygame

from settings import *

class Wall(pygame.sprite.Sprite):
    def __init__(self, game , x, y):
        self._layer = 1
        self.groups = (game.sprites, game.walls)
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.image = pygame.Surface((TILE_SIZE, TILE_SIZE))
        self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)