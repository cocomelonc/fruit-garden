# -*- coding: utf-8 -*-
import pygame

class WeaponFireSprite(pygame.sprite.Sprite):
    def __init__(self, screen, last_direction, x, y):
        super(WeaponFireSprite, self).__init__()
        self.x, self.y = x, y
        self.last_direction = last_direction
        self.screen = screen
        self.left, self.right, self.up, self.down = [], [], [], []
        for i in range(6):
            self.right.append(pygame.image.load("./images/enemies/weapon-fire-right_{}.png".format(i+1)))
            self.left.append(pygame.image.load("./images/enemies/weapon-fire-left_{}.png".format(i+1)))
            self.up.append(pygame.image.load("./images/enemies/weapon-fire-up_{}.png".format(i+1)))
            self.down.append(pygame.image.load("./images/enemies/weapon-fire-down_{}.png".format(i+1)))
        self.index = 0
        self.image = self.right[self.index]
        self.rect = pygame.Rect(self.x, self.y, 32, 32)

    def update(self):
        self.index += 1
        if self.index >= len(self.left) * 20:
            self.index = 0
        if self.index % 20 == 0:
            if self.last_direction == 'left':
                self.image = self.left[int(self.index/20)]
            elif self.last_direction == 'right':
                self.image = self.right[int(self.index/20)]
            elif self.last_direction == 'up':
                self.image = self.up[int(self.index/20)]
            elif self.last_direction == 'down':
                self.image = self.down[int(self.index/20)]
        super(WeaponFireSprite, self).update()

# enemy's weapon class (fire)
class WeaponFire(pygame.sprite.Group):
    def __init__(self, screen, enemy):
        self.enemy, self.screen = enemy, screen
        self.drawing, self.last_direction = False, self.enemy.face
        if self.last_direction == 'left':
            self.x, self.y = self.enemy.x, self.enemy.y
        elif self.last_direction == 'right':
            self.x, self.y = self.enemy.x + 4, self.enemy.y
        elif self.last_direction == 'up':
            self.x, self.y = self.enemy.x + 2, self.enemy.y
        elif self.last_direction == 'down':
            self.x, self.y = self.enemy.x, self.enemy.y + 4
        self.rect = pygame.Rect(self.x, self.y, 32, 32)
        self.centerx, self.centery = self.rect.center
        self.weapon_fire_sprite = WeaponFireSprite(self.screen, self.last_direction, self.x, self.y)
        super(WeaponFire, self).__init__(self.weapon_fire_sprite)

    def draw(self):
        if self.drawing:
            self.screen.blit(self.weapon_fire_sprite.image, [self.x, self.y])

    def update(self):
        self.centerx, self.centery = self.rect.center
        if self.drawing:
            if self.last_direction == 'left':
                if self.x >= 2:
                    self.x -= 0.5
            elif self.last_direction == 'right':
                if self.x <= 632:
                    self.x += 0.5
            elif self.last_direction == 'up':
                if self.y >= 2:
                    self.y -= 0.5
            elif self.last_direction == 'down':
                if self.y <= 632:
                    self.y += 0.5
            if self.x <= 4 or self.x >= 632 or self.y <= 4 or self.y >= 632:
                self.drawing = False
                self.last_direction = self.enemy.face
                if self.enemy.face == 'left':
                    self.x, self.y = self.enemy.x, self.enemy.y
                elif self.enemy.face == 'right':
                    self.x, self.y = self.enemy.x + 4, self.enemy.y
                elif self.enemy.face == 'up':
                    self.x, self.y = self.enemy.x + 2, self.enemy.y
                elif self.enemy.face == 'down':
                    self.x, self.y = self.enemy.x, self.enemy.y + 4
        else:
            self.last_direction = self.enemy.face
            if self.enemy.face == 'left':
                self.x, self.y = self.enemy.x, self.enemy.y
            elif self.enemy.face == 'right':
                self.x, self.y = self.enemy.x + 4, self.enemy.y
            elif self.enemy.face == 'up':
                self.x, self.y = self.enemy.x + 2, self.enemy.y
            elif self.enemy.face == 'down':
                self.x, self.y = self.enemy.x, self.enemy.y + 4
        self.rect = pygame.Rect(self.x, self.y, 32, 32)
        super(WeaponFire, self).update()

