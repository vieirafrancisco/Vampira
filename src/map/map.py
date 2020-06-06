import os
import pygame

from settings import *
from src.sprites.player import Player
from src.sprites.map_sprites import Wall

class Map:
    def __init__(self, game, path_folder):
        self.game = game
        self.path_folder = path_folder
        self.images = os.listdir(path_folder)
        self.curr_map = 0
        self.limit = len(self.images)
        self.map_arr = []

    def draw(self):
        pass

    def shift_map(self):
        self.curr_map += 1
        self.curr_map %= self.limit
