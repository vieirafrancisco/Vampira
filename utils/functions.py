import pygame

from settings import *

def euclidian_distance(a, b):
    def func(pos):
        x, y = pos
        return (x - y) ** 2
    return sum(map(func, zip(a, b)))

def similarity(color):
    color_tuple = (color.r, color.g, color.b)
    m = INF
    res = BLACK
    for global_color in COLOR_LIST:
        d = euclidian_distance(color_tuple, global_color)
        if d < m:
            m = d
            res = global_color
    return res

def get_map_by_image(image_path):
    img = pygame.image.load(image_path)
    w, h = img.get_size()
    map_array = [['' for i in range(h)] for j in range(w)]
    for i in range(w):
        for j in range(h):
            image_color = img.get_at((i, j))
            similar_color = similarity(image_color)
            if similar_color == BROWN:
                map_array[i][j] = "WALL"
            elif similar_color == BLUE:
                map_array[i][j] = "PLAYER"
    return map_array