import pygame
from pygame.locals import *

from settings import *

class Game:
    def __init__(self):
        self.running = False
        self.surface = None
        self.clock = pygame.time.Clock()

    def init(self):
        pygame.init()
        self.running = True
        self.surface = pygame.display.set_mode((WIDTH, HEIGHT))

    def cleanup(self):
        pygame.quit()

    def render(self):
        pass

    def loop(self):
        pass

    def event(self, event):
        if event.type == QUIT:
            self.running = False

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