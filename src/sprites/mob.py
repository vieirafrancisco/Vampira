import random

import pygame

from settings import *

class Mob(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = (game.mobs)
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pygame.Surface((TILE_SIZE, TILE_SIZE))
        self.image.fill(BLUE)
        self.rect = self.image.get_rect()
        self.rect.topleft = (x * TILE_SIZE, y * TILE_SIZE)
        self.pos = (x, y)
        self.is_moving = False
        self.target_node = (0, 0)
        self.dir = (1, 0)
        self.possible_directions = []

    def update(self):
        if not self.is_moving:
            self.possible_directions = list(filter(lambda p: self.game.is_node((p[0] + self.pos[0], p[1] + self.pos[1])), DIRECTIONS))
            self.dir = random.choice(self.possible_directions)
            self.is_moving = True
            self.target_node = (self.pos[0] + self.dir[0], self.pos[1] + self.dir[1])
        else:
            if (self.rect.x / TILE_SIZE, self.rect.y / TILE_SIZE) != self.target_node:
                self.rect.x += MOB_SPEED * self.dir[0]
                self.rect.y += MOB_SPEED * self.dir[1]
            else:
                self.is_moving = False
                self.game.swap_entity_position(self.pos, (self.rect.x // TILE_SIZE, self.rect.y // TILE_SIZE))
                self.pos = (self.rect.x // TILE_SIZE, self.rect.y // TILE_SIZE)
                has_player = self.verify_sides()
                if not has_player:
                    print("not has player!")
                else:
                    print("has player!")

    def verify_sides(self):
        for d in filter(lambda x: x != self.dir, self.possible_directions):
            x = self.pos[0] + d[0]
            y = self.pos[1] + d[1]
            while self.game.map_array[x][y] != WALL:
                if self.game.map_array[x][y] == PLAYER:
                    return True
                x = x + d[0]
                y = y + d[1]
        return False
 
        