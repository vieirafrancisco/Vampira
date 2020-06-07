import pygame

from settings import *

class Wall(pygame.sprite.Sprite):
    def __init__(self, game , x, y):
        self._layer = WALL_LAYER
        self.groups = (game.sprites, game.walls)
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pygame.Surface((TILE_SIZE, TILE_SIZE))
        self.image.blit(game.wall_image, (0, 0))
        self.rect = self.image.get_rect()
        self.rect.topleft = (x * TILE_SIZE, y * TILE_SIZE)