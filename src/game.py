import os

import pygame
from pygame.locals import *

from settings import *
from src.sprites.player import Player
from src.sprites.map_sprites import Wall
from utils.functions import get_map_by_image, dijkstra, get_two_nodes_distance

class Game:
    def __init__(self):
        self.running = False
        self.surface = None
        self.clock = pygame.time.Clock()

    def init(self):
        pygame.init()
        self.running = True
        self.surface = pygame.display.set_mode((WIDTH, HEIGHT))
        self.display_grid = True
        self.sprites = pygame.sprite.LayeredUpdates()
        self.walls = pygame.sprite.Group()
        self.map_array = get_map_by_image(os.path.join("resources", "maps", "map01.png"))
        for i, row in enumerate(self.map_array):
            for j, col in enumerate(row):
                if self.map_array[i][j] == WALL:
                    Wall(self, i, j)
                elif self.map_array[i][j] == PLAYER:
                    self.player = Player(self, i, j)
        self.make_graph()

    def is_node(self, coord):
        x, y = coord
        if self.map_array[x][y] not in NOT_NODES:
            return True
        else:
            return False

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
        self.dists = dijkstra(self.player.pos, self.graph)

    def cleanup(self):
        pygame.quit()

    def render(self):
        self.sprites.draw(self.surface)
        if self.display_grid:
            for i in range(0, WIDTH, TILE_SIZE):
                pygame.draw.line(self.surface, GRAY, (i, 0), (i, HEIGHT))
            for j in range(0, HEIGHT, TILE_SIZE):
                pygame.draw.line(self.surface, GRAY, (0, j), (WIDTH, j))

    def loop(self):
        self.sprites.update()

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
            self.surface.fill(BLACK)
            self.render()
            self.loop()
            pygame.display.flip()
            self.clock.tick(FPS)
            pygame.display.set_caption(f"Vampira - FPS: {round(self.clock.get_fps(), 2)}")
        self.cleanup()