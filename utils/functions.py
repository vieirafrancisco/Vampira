import os
import heapq

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


def get_map_by_image(map_image):
    w, h = map_image.get_size()
    map_array = [[EMPTY for i in range(h)] for j in range(w)]
    for i in range(w):
        for j in range(h):
            image_color = map_image.get_at((i, j))
            similar_color = similarity(image_color)
            if similar_color == BROWN:
                map_array[i][j] = WALL
            elif similar_color == BLUE:
                map_array[i][j] = PLAYER
            elif similar_color == GREEN:
                map_array[i][j] = MOB
            elif similar_color == RED:
                map_array[i][j] = STAIRS
    return map_array


def get_two_nodes_distance(n1: tuple, n2: tuple) -> int:
    """
    Function to calculate the distance between two nodes (tiles)
    n1, n1: tuple(x, y)
    return: an integer representing the distance between the two nodes
    """
    dx = abs(n2[0] - n1[0])
    dy = abs(n2[1] - n1[1])
    return sum([dx, dy])


def dijkstra(p, graph):
    """
    p: player position
    graph: dictionary of adjancences
    return: list of distances and the path to a target node
    """
    n = len(graph)
    dist = {key: INF for key in graph.keys()}
    visited = {key: False for key in graph.keys()}
    origin = {key: -1 for key in graph.keys()}
    dist[p] = 0
    p_queue = []
    heapq.heappush(p_queue, (0, p))
    while p_queue:
        u = heapq.heappop(p_queue)
        visited[u[1]] = True
        for v in graph[u[1]]:
            if not visited[v[1]] and u[0] + v[0] < dist[v[1]]:
                dist[v[1]] = u[0] + v[0]
                origin[v[1]] = u[1]
                heapq.heappush(p_queue, (dist[v[1]], v[1]))

    def get_paths():
        paths = {key: [] for key in origin.keys()}
        for node in origin.keys():
            value = origin[node]
            while value != -1:
                paths[node].append(value)
                value = origin[value]
            paths[node].reverse()
        return paths

    return dist, get_paths()


def memset(value, size):
    return [value for _ in range(size)]


def footprint_angle(target: tuple, path: list) -> int:
    """
        Function that returns the angle of the footprint sprite.
        The start point of the sprite is in the bottom direction, them the y = 1 it's already taken with 0 rotation.
        target: tuple with the x and y coordinates of the target node
        path: a list of tuples (coordenates), that have the path from the player position a mouse clicked node
        return: a integer (angle)
    """
    target_pos = vec(target)
    prev_pos = vec(path[-1])
    footprint_dir = target_pos - prev_pos
    if footprint_dir.x == 1:
        return 90
    elif footprint_dir.x == -1:
        return -90
    elif footprint_dir.y == -1:
        return 180
    return 0


def load_image(file_name: str, folder="spritesheets"):
    return pygame.image.load(os.path.join(RESOURCE_PATHS[folder], file_name))
