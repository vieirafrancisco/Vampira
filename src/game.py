import os
import time

import pygame
from pygame.locals import *

from settings import *
from src.sprites.player import Player
from src.sprites.map_sprites import Wall
from src.sprites.mob import Mob
from utils.functions import get_map_by_image, dijkstra, get_two_nodes_distance, memset

class Game:
    def __init__(self):
        self.running = False
        self.surface = None
        self.clock = pygame.time.Clock()

    def init(self):
        pygame.init()
        self.running = True
        self.surface = pygame.display.set_mode((WIDTH, HEIGHT))
        self.display_grid = False
        self.in_turn = True
        self.sprites = pygame.sprite.LayeredUpdates()
        self.walls = pygame.sprite.Group()
        self.mobs = pygame.sprite.Group()
        self.player_image = pygame.image.load(os.path.join("resources", "spritesheets", "vampira_spritesheet_01.png"))
        self.wall_image = pygame.image.load(os.path.join("resources", "spritesheets", "castle_wall_2.png"))
        self.mob_image = pygame.image.load(os.path.join("resources", "spritesheets", "mob_spritesheet_1.png"))
        self.map_array = get_map_by_image(os.path.join("resources", "maps", "map_1.png"))
        for i, row in enumerate(self.map_array):
            for j, col in enumerate(row):
                if self.map_array[i][j] == WALL:
                    Wall(self, i, j)
                elif self.map_array[i][j] == MOB:
                    Mob(self, i, j)
                elif self.map_array[i][j] == PLAYER:
                    self.player = Player(self, i, j)
        self.make_graph()

    def is_node(self, coord):
        x, y = coord
        if self.map_array[x][y] not in NOT_NODES:
            return True
        else:
            return False
    
    def swap_entity_position(self, pos_a, pos_b):
        xa, ya = pos_a
        xb, yb = pos_b
        self.map_array[xa][ya], self.map_array[xb][yb] = self.map_array[xb][yb], self.map_array[xa][ya]

    def make_graph(self):
        self.graph = {}
        h = len(self.map_array)
        w = len(self.map_array[0])
        def func(pos):
            x, y = pos
            return x >= 0 and x < h and y >= 0 and y < w and self.is_node((x, y))
        for i in range(h):
            for j in range(w):
                if self.is_node((i, j)):
                    values = map(lambda x: (1, x), filter(func, [(i, j-1), (i+1, j), (i, j+1), (i-1,j)]))
                    self.graph[(i, j)] = list(values)
        self.dists, self.origins = dijkstra(self.player.pos, self.graph)
        def get_paths():
            paths = {key: [] for key in self.origins.keys()}
            for node in self.origins.keys():
                value = self.origins[node]
                while value != -1:
                    paths[node].append(value)
                    value = self.origins[value]
                paths[node].reverse()
            return paths
        self.paths = get_paths()
        
    def cleanup(self):
        pygame.quit()

    def render(self):
        self.sprites.draw(self.surface)
        self.mobs.draw(self.surface)
        if self.display_grid:
            for i in range(0, CANVAS_WIDTH, TILE_SIZE):
                pygame.draw.line(self.surface, GRAY, (i, 0), (i, CANVAS_HEIGHT))
            for j in range(0, CANVAS_HEIGHT, TILE_SIZE):
                pygame.draw.line(self.surface, GRAY, (0, j), (CANVAS_WIDTH, j))
        if not self.player.is_moving and self.in_turn:
            dists_gt_zero_and_leq_player_wr = list(filter(lambda x: 0 < x[1] <= self.player.walk_range and self.is_node(x[0]), self.dists.items()))
            for node, _ in dists_gt_zero_and_leq_player_wr:
                x, y = node
                surface = pygame.Surface((TILE_SIZE, TILE_SIZE), pygame.SRCALPHA)
                surface.fill((0, 255, 0, 75))
                self.surface.blit(surface, (x * TILE_SIZE, y * TILE_SIZE))
        # HUD - inventory
        y = CANVAS_HEIGHT
        for x in range(0, WIDTH, 32):
            pygame.draw.rect(self.surface, DARK_GRAY, (x, y, TILE_SIZE, TILE_SIZE))
            pygame.draw.rect(self.surface, BLACK, (x, y, TILE_SIZE, TILE_SIZE), 3)

    def loop(self):
        if self.in_turn:
            self.sprites.update()
            self.mobs_turn_state = memset(0, len(self.mobs.sprites()))
        else:
            self.mobs.update()
            for idx, mob in enumerate(self.mobs.sprites()):
                if not mob.is_moving:
                    self.mobs_turn_state[idx] = 1
            if all(self.mobs_turn_state):
                self.in_turn = True
                self.make_graph()
                self.mobs_turn_state = memset(0, len(self.mobs.sprites()))

    def event(self, event):
        if event.type == QUIT:
            self.running = False
        if event.type == KEYDOWN:
            if event.key == K_p:
                self.display_grid = not self.display_grid

    def execute(self):
        self.init()
        while self.running:
            for event in pygame.event.get():
                self.event(event)
            self.surface.fill(DARK_BLUE)
            self.render()
            self.loop()
            pygame.display.flip()
            self.clock.tick(FPS)
            pygame.display.set_caption(f"Vampira - FPS: {round(self.clock.get_fps(), 2)}")
        self.cleanup()