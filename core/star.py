# -*- coding: utf-8 -*-
import pygame

# star - collect by player
class Star():
    def __init__(self, screen, x, y):
        self.image = pygame.image.load("./images/hero/star.png")
        self.x, self.y = x, y
        self.screen = screen
        self.drawing = True

    def draw(self):
        if self.drawing:
            self.screen.blit(self.image, [self.x, self.y])
