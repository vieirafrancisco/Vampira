import os
import sys

import pygame
from pygame.locals import *

from settings import *
from src.sprites.player import Player
from src.sprites.map_sprites import Wall
from src.sprites.mob import Mob
from utils.functions import get_map_by_image, dijkstra, get_two_nodes_distance, memset

class Game:
    def __init__(self):
        pygame.init()
        pygame.font.init()
        self.running = False
        self.surface = pygame.display.set_mode((WIDTH, HEIGHT))
        self.clock = pygame.time.Clock()
        self.load_data()

    def load_data(self):
        self.player_image = pygame.image.load(os.path.join("resources", "spritesheets", "vampira_spritesheet_01.png"))
        self.wall_image = pygame.image.load(os.path.join("resources", "spritesheets", "castle_wall_2.png"))
        self.mob_image = pygame.image.load(os.path.join("resources", "spritesheets", "mob_spritesheet_1.png"))

    def new(self):
        self.display_grid = False
        self.in_turn = True
        self.sprites = pygame.sprite.LayeredUpdates()
        self.walls = pygame.sprite.Group()
        self.mobs = pygame.sprite.Group()
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

    def cleanup(self):
        pygame.font.quit()
        pygame.quit()
        sys.exit()

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
        if not self.player.is_moving and self.in_turn:
            dists_gt_zero_and_leq_player_wr = list(filter(lambda x: 0 < x[1] <= self.player.walk_range and self.is_node(x[0]), self.dists.items()))
            for node_position, _ in dists_gt_zero_and_leq_player_wr:
                x, y = node_position
                footprint_surface = pygame.image.load(os.path.join("resources", "spritesheets", "seta.png")).convert()
                footprint_surface.set_colorkey(COLOR_KEY)
                # rotate footprints sprites
                prev_pos = self.paths[x, y][-1]
                footprint_dir = (x - prev_pos[0], y - prev_pos[1])
                if footprint_dir[0] == 1:
                    footprint_surface = pygame.transform.rotate(footprint_surface, 90)
                elif footprint_dir[0] == -1:
                    footprint_surface = pygame.transform.rotate(footprint_surface, -90)
                elif footprint_dir[1] == -1:
                    footprint_surface = pygame.transform.rotate(footprint_surface, 180)
                px, py = map(lambda coord: coord * TILE_SIZE, node_position)
                self.surface.blit(footprint_surface, (px, py))
                mx, my = pygame.mouse.get_pos()
                if mx >= px and mx < px + TILE_SIZE and my >= py and my < py + TILE_SIZE:
                    fp_path = self.paths[x, y][1:]
                    fp_path.append((x, y))
                    for fp_x, fp_y in fp_path:
                        green_color_surface = pygame.Surface((TILE_SIZE, TILE_SIZE), SRCALPHA)
                        green_color_surface.fill((0, 240, 0, 75))
                        self.surface.blit(green_color_surface, (fp_x * TILE_SIZE, fp_y * TILE_SIZE))
                    pygame.draw.rect(self.surface, DARK_GREEN, (px, py, TILE_SIZE, TILE_SIZE), 2)
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