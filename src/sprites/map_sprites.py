import pygame

from settings import *


class Wall(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        self._layer = WALL_LAYER
        self.groups = (game.sprites, game.walls)
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pygame.Surface((TILE_SIZE, TILE_SIZE))
        self.image.blit(game.wall_image, (0, 0))
        self.rect = self.image.get_rect()
        self.rect.topleft = (x * TILE_SIZE, y * TILE_SIZE)


class Item(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        self._layer = ITEM_LAYER
        self.game = game
        self.groups = (game.sprites, game.items)
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.image = pygame.Surface((TILE_SIZE, TILE_SIZE))
        self.rect = self.image.get_rect()
        self.rect.topleft = (x * TILE_SIZE, y * TILE_SIZE)
        self.pos = (x, y)


class Endpoint(Item):
    def __init__(self, game, x, y):
        Item.__init__(self, game, x, y)
        self.image.blit(game.stairs_image, (0, 0))

    def update(self):
        if self.pos == self.game.player.pos:
            self.game.change_map()
            return True
