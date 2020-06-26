import os
import sys

import pygame
from pygame.locals import *

from settings import *
from src.sprites.player import Player
from src.sprites.map_sprites import Wall, Endpoint
from src.sprites.mob import Mob
from src.map.map import Map
from utils.functions import get_map_by_image, dijkstra, memset, load_image


class Game:
    def __init__(self):
        pygame.init()
        pygame.font.init()
        self.running = False
        self.surface = pygame.display.set_mode((WIDTH, HEIGHT))
        self.clock = pygame.time.Clock()
        self.map_count = 0
        self.load_data()
        self.player = None
        self.map = Map.create_map(self)

    def load_data(self):
        self.player_image = load_image("vampira_spritesheet_01.png")
        self.wall_image = load_image("castle_wall_2.png")
        self.mob_image = load_image("mob_spritesheet_1.png")
        self.stairs_image = load_image("stairs.png")

    def new(self):
        self.display_grid = False
        self.in_turn = True
        self.turn = 0
        self.sprites = pygame.sprite.LayeredUpdates()
        self.walls = pygame.sprite.Group()
        self.mobs = pygame.sprite.Group()
        self.items = pygame.sprite.Group()
        self.entities = pygame.sprite.Group()
        self.map.update_data()
        for i, row in enumerate(self.map.data):
            for j, col in enumerate(row):
                if self.map.data[i][j] == WALL:
                    Wall(self, i, j)
                elif self.map.data[i][j] == MOB:
                    Mob(self, i, j)
                elif self.map.data[i][j] == STAIRS:
                    Endpoint(self, i, j)
                elif self.map.data[i][j] == PLAYER:
                    self.player = Player(self, i, j)
        self.map.update()

    def cleanup(self):
        pygame.font.quit()
        pygame.quit()
        sys.exit()


    def render(self):
        # draw entity sprites
        self.sprites.draw(self.surface)
        self.mobs.draw(self.surface)
        # debug grid
        if self.display_grid:
            for i in range(0, CANVAS_WIDTH, TILE_SIZE):
                pygame.draw.line(self.surface, GRAY, (i, 0), (i, CANVAS_HEIGHT))
            for j in range(0, CANVAS_HEIGHT, TILE_SIZE):
                pygame.draw.line(self.surface, GRAY, (0, j), (CANVAS_WIDTH, j))
        # movement HUD        
        if not self.player.is_moving and self.in_turn:
            for entity in self.entities.sprites():
                dists = self.map.entities_path_find[entity][0]
                dists_gt_zero_and_leq_entity_vr = list(
                    filter(lambda dist: 0 < dist[1] <= entity.vision_range and self.map.is_node(*dist[0]),
                           dists.items()))
                for (x, y), _ in dists_gt_zero_and_leq_entity_vr:
                    entity.draw_vision(x, y)
        # HUD - inventory
        y = CANVAS_HEIGHT
        for x in range(0, WIDTH, 32):
            pygame.draw.rect(self.surface, DARK_GRAY, (x, y, TILE_SIZE, TILE_SIZE))
            pygame.draw.rect(self.surface, BLACK, (x, y, TILE_SIZE, TILE_SIZE), 3)
        # Information text
        self.draw_text(f"Map: {self.map.curr_map}", WHITE, 10, 0, 18)
        self.draw_text(f"Turn: {self.turn}", WHITE, 10, 30, 18)

    def loop(self):
        if self.in_turn:
            self.sprites.update()
            for mob in self.mobs.sprites():
                if vec(self.player.pos) + vec(mob.dir) == vec(mob.pos):
                    x, y = mob.pos
                    self.map.data[x][y] = EMPTY
                    mob.kill()
            self.mobs_turn_state = memset(0, len(self.mobs.sprites()))
        else:
            for mob in self.mobs.sprites():
                for p in self.player.path_list:
                    if mob.has_vision_in_position(*p):
                        self.running = False
                        break
            self.mobs.update()
            for idx, mob in enumerate(self.mobs.sprites()):
                if not mob.is_moving:
                    self.mobs_turn_state[idx] = 1
            if all(self.mobs_turn_state):
                self.in_turn = True
                self.turn += 1
                self.map.update()
                self.mobs_turn_state = memset(0, len(self.mobs.sprites()))
                for mob in self.mobs.sprites():
                    if mob.has_vision_in_position(*self.player.pos):
                        self.running = False

    def event(self, event):
        if event.type == QUIT:
            self.cleanup()
        if event.type == KEYDOWN:
            if event.key == K_p:
                self.display_grid = not self.display_grid

    def execute(self):
        self.running = True
        while self.running:
            for event in pygame.event.get():
                self.event(event)
            self.surface.fill(DARK_BLUE)
            self.render()
            self.loop()
            pygame.display.flip()
            self.clock.tick(FPS)
            pygame.display.set_caption(f"Vampira - FPS: {round(self.clock.get_fps(), 2)}")

    def menu_screen(self):
        pass

    def game_over_screen(self):
        self.surface.fill(BLACK)
        self.draw_text("Game Over", RED, WIDTH // 4, 2 * HEIGHT // 5, 30)
        self.draw_text("Press any key to continue!", WHITE, WIDTH // 5, 2 * HEIGHT // 5 + 40, 15)
        pygame.display.flip()
        self.wait_any_key()

    def wait_any_key(self):
        # reference code: https://github.com/kidscancode/pygame_tutorials/blob/master/tilemap/part%2022/main.py
        pygame.event.wait()
        waiting = True
        while waiting:
            self.clock.tick(FPS)
            for event in pygame.event.get():
                if event.type == QUIT:
                    waiting = False
                    self.cleanup()
                if event.type == KEYUP or event.type == MOUSEBUTTONUP:
                    waiting = False

    def draw_text(self, text, color, x, y, size, font_name='Comic Sans MS'):
        font = pygame.font.SysFont(font_name, size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        text_rect.topleft = (x, y)
        self.surface.blit(text_surface, text_rect)
