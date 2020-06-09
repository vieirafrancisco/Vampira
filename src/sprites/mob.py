import os
import random
import json

import pygame

from settings import *

class Mob(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = (game.mobs)
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pygame.Surface((TILE_SIZE, TILE_SIZE))
        self.image.blit(self.game.mob_image, (0, 0), (1 * TILE_SIZE, 0 * TILE_SIZE, TILE_SIZE, TILE_SIZE))
        self.image.set_colorkey(COLOR_KEY)
        self.rect = self.image.get_rect()
        self.rect.topleft = (x * TILE_SIZE, y * TILE_SIZE)
        self.pos = (x, y)
        self.is_moving = False
        self.target_node = (0, 0)
        self.dir = (1, 0)
        self.possible_directions = []
        self.last_update = pygame.time.get_ticks()
        self.animation_count = 0
        self.load_images()

    def load_images(self):
        self.images = {}
        with open(os.path.join("resources", "json", "mob_spritesheet_1.json"), "r") as f:
            player_image_pos = json.load(f)
        spritesheet = self.game.mob_image
        for image_name, pos in player_image_pos.items():
            self.images[image_name] = pygame.Surface((TILE_SIZE, TILE_SIZE)).convert()
            self.images[image_name].blit(spritesheet, (0, 0), (pos[0] * TILE_SIZE, pos[1] * TILE_SIZE, TILE_SIZE, TILE_SIZE))
            self.images[image_name].set_colorkey(COLOR_KEY)

    def animate(self):
        now = pygame.time.get_ticks()
        if self.is_moving and now - self.last_update >= 150:
            self.last_update = now
            x, y = self.dir
            if x or y:
                if x == 1:
                    self.image = self.images[f"right_{self.animation_count}"]
                elif x == -1:
                    self.image = self.images[f"left_{self.animation_count}"]
                elif y == 1:
                    self.image = self.images[f"down_{self.animation_count}"]
                elif y == -1:
                    self.image = self.images[f"up_{self.animation_count}"]
                self.animation_count = (self.animation_count + 1) % 2

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
                if self.dir[0] == 1:
                    self.image = self.images["right_stand"]
                elif self.dir[0] == -1:
                    self.image = self.images["left_stand"]
                elif self.dir[1] == 1:
                    self.image = self.images["down_stand"]
                elif self.dir[1] == -1:
                    self.image = self.images["up_stand"]
                if not has_player:
                    print("not has player!")
                else:
                    print("has player!")
        self.animate()

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
 
        