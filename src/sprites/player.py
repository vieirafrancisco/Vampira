import os
import math
import json

import pygame

from settings import *
from utils.functions import get_two_nodes_distance


def inside_canvas(x, y):
    if x * TILE_SIZE < CANVAS_WIDTH and y * TILE_SIZE < CANVAS_HEIGHT:
        return True
    else:
        return False


def get_movement_list(path_list):
    movement_list = []
    for a, b in zip(path_list[:-1], path_list[1:]):
        movement_list.append((b[0] - a[0], b[1] - a[1]))
    return movement_list


class Player(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        self._layer = PLAYER_LAYER
        self.groups = (game.sprites, game.entities)
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pygame.Surface((PLAYER_WIDTH, PLAYER_HEIGHT)).convert()
        self.image.blit(self.game.player_image, (0, 0),
                        (1 * PLAYER_WIDTH, 0 * PLAYER_HEIGHT, PLAYER_WIDTH, PLAYER_HEIGHT))
        self.image.set_colorkey(COLOR_KEY)
        self.rect = self.image.get_rect()
        self.rect.topleft = (x * PLAYER_WIDTH, y * PLAYER_HEIGHT)
        self.pos = (x, y)
        self.walk_range = PLAYER_WALK_RANGE
        self.load_images()
        self.movement_list = []
        self.is_moving = False
        self.target_node = (0, 0)
        self.curr_node = (0, 0)
        self.last_update = pygame.time.get_ticks()
        self.animation_count = 0

    def load_images(self):
        self.images = {}
        with open(os.path.join("resources", "json", "vampira_spritesheet_01.json"), "r") as f:
            player_image_pos = json.load(f)
        spritesheet = self.game.player_image
        size = (PLAYER_WIDTH, PLAYER_HEIGHT)
        for image_name, pos in player_image_pos.items():
            self.images[image_name] = pygame.Surface((size)).convert()
            self.images[image_name].blit(spritesheet, (0, 0), (pos[0] * size[0], pos[1] * size[1], size[0], size[1]))
            self.images[image_name].set_colorkey(COLOR_KEY)

    def animate(self):
        now = pygame.time.get_ticks()
        if now - self.last_update >= 150:
            self.last_update = now
            x, y = self.curr_node
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
        mouse_click = pygame.mouse.get_pressed()[0]
        if mouse_click:
            mouse_pos = pygame.mouse.get_pos()
            x = math.floor(mouse_pos[0] / TILE_SIZE)
            y = math.floor(mouse_pos[1] / TILE_SIZE)
            if inside_canvas(x, y) and self.game.map_array[x][y] not in NOT_NODES:
                d = self.game.dists[(x, y)]
                if 0 < d <= self.walk_range and not self.is_moving:
                    path_list = self.game.paths[x, y].copy()
                    path_list.append((x, y))
                    self.movement_list = get_movement_list(path_list)
                    self.target_node = (x, y)
                    self.is_moving = True
        if self.is_moving:
            if self.rect.x % TILE_SIZE == 0 and self.rect.y % TILE_SIZE == 0 and self.movement_list != []:
                self.curr_node = self.movement_list[0]
                self.movement_list = self.movement_list[1:]
            if (self.rect.x / TILE_SIZE, self.rect.y / TILE_SIZE) == self.target_node:
                self.is_moving = False
                self.curr_node = (0, 0)
                self.game.swap_entity_position(self.pos, self.target_node)
                self.pos = self.target_node
                x, y = self.pos
                last_node = self.game.paths[x, y][-1]
                self.game.make_graph()
                if x - last_node[0] == 1:
                    self.image = self.images["right_stand"]
                elif x - last_node[0] == -1:
                    self.image = self.images["left_stand"]
                elif y - last_node[1] == 1:
                    self.image = self.images["down_stand"]
                elif y - last_node[1] == -1:
                    self.image = self.images["up_stand"]
                self.game.in_turn = False
            else:
                self.rect.x += PLAYER_SPEED * self.curr_node[0]
                self.rect.y += PLAYER_SPEED * self.curr_node[1]
        self.animate()
