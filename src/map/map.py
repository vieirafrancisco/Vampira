import os

import pygame
from pygame.locals import *

from settings import *
from utils.functions import load_image, get_map_by_image, get_directions, dijkstra


class Map:
    def __init__(self, game):
        self.game = game
        self.curr_map = 0
        self.limit = len(os.listdir(MAPS_FOLDER_PATH))
        self.data = []
        self.graph = {}
        self.entities_path_find = {}

    @staticmethod
    def create_map(game):
        m = Map(game)
        m.update_data()
        return m

    def update_data(self):
        image = pygame.image.load(os.path.join(MAPS_FOLDER_PATH, f"map_{self.curr_map}.png"))
        self.data = get_map_by_image(image)

    def change_map(self):
        self.curr_map = (self.curr_map + 1) % self.limit
        self.update_data()
        self.game.new()

    def is_node(self, x, y):
        return self.data[x][y] not in NOT_NODES

    def make_graph(self):
        height = len(self.data)
        width = len(self.data[0])

        def func(pos):
            x, y = pos
            return 0 <= x < height and 0 <= y < width and self.is_node(x, y)

        for i in range(height):
            for j in range(width):
                if self.is_node(i, j):
                    values = map(lambda x: (1, x), filter(func, get_directions(i, j)))
                    self.graph[(i, j)] = list(values)

    def path_find(self, entity):
        if self.graph:
            return dijkstra(entity.pos, self.graph)

    def update(self):
        self.make_graph()
        self.entities_path_find = {}
        for entity in self.game.entities.sprites():
            self.entities_path_find[entity] = self.path_find(entity)

    def swap_entity_position(self, pos_a, pos_b):
        xa, ya = pos_a
        xb, yb = pos_b
        self.data[xa][ya], self.data[xb][yb] = self.data[xb][yb], self.data[xa][ya]
