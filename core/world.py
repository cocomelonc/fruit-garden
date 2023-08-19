# -*- coding: utf-8 -*-
import pygame
import sys
import random
from core.level import *

class World():
    SIZE = (640, 640)

    def __init__(self):
        pygame.init()
        self.clock = pygame.time.Clock()
        self.icon_img = pygame.image.load("./images/levels/game.png")
        pygame.display.set_caption('Fruit garden')
        pygame.display.set_icon(self.icon_img)
        self.pause = False
        self.pygame = pygame
        self.screen = pygame.display.set_mode(self.SIZE)
        self.level = Level(self, 1)

    def draw(self):
        self.level.draw()

    def update(self):
        if self.pause == False:
            self.level.update()

    def play(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_p:
                        self.pause = not self.pause
            key = pygame.key.get_pressed()
            if key[pygame.K_ESCAPE]:
                sys.exit()
            self.draw()
            self.update()
            pygame.display.flip()
            self.clock.tick(240)
        pygame.quit()
