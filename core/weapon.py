# -*- coding: utf-8 -*-
import pygame

# apple flight speed in pixels per frame (game runs at 240 FPS).
# Kept in scale with hero STEP=0.25 and enemy fire 0.5 — the old value of 4
# crossed the whole screen in ~0.6s, too fast to see.
APPLE_SPEED = 0.75

# player's weapon class (apple)
class Weapon():
    def __init__(self, screen, hero):
        self.hero = hero
        self.image = pygame.image.load("./images/hero/apple-player.png")
        self.x, self.y = self.hero.x - 6, self.hero.y + 4
        self.rect = pygame.Rect(self.x, self.y, 16, 16)
        self.centerx, self.centery = self.rect.center
        self.screen = screen
        self.drawing, self.last_direction = False, self.hero.face

    def draw(self):
        if self.drawing:
            self.screen.blit(self.image, [self.x, self.y])

    def update(self):
        self.rect = pygame.Rect(self.x, self.y, 16, 16)
        self.centerx, self.centery = self.rect.center
        if self.drawing:
            if self.last_direction == 'left':
                if self.x >= 2:
                    self.x -= APPLE_SPEED
            elif self.last_direction == 'right':
                if self.x <= 632:
                    self.x += APPLE_SPEED
            elif self.last_direction == 'up':
                if self.y >= 2:
                    self.y -= APPLE_SPEED
            elif self.last_direction == 'down':
                if self.y <= 632:
                    self.y += APPLE_SPEED
            if self.x <= 4 or self.x >= 632 or self.y <= 4 or self.y >= 632:
                self.drawing = False
                self.last_direction = self.hero.face
        else:
            self.last_direction = self.hero.face
            if self.hero.face == 'left':
                self.x, self.y = self.hero.x + 12, self.hero.y + 16
            elif self.hero.face == 'right':
                self.x, self.y = self.hero.x + 12, self.hero.y + 16
            elif self.hero.face == 'up':
                self.x, self.y = self.hero.x + 12, self.hero.y + 16
            elif self.hero.face == 'down':
                self.x, self.y = self.hero.x + 12, self.hero.y + 16

