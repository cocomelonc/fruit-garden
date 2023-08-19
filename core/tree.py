# -*- coding: utf-8 -*-
import pygame

# Tree sprite
class TreeSprite(pygame.sprite.Sprite):
    def __init__(self, screen, x, y):
        super(TreeSprite, self).__init__()
        self.x, self.y = x, y
        self.screen = screen
        self.images = []
        self.images.append(pygame.image.load("./images/resources/tree.png"))
        self.images.append(pygame.image.load("./images/resources/tree-apple.png"))
        self.index = 0
        self.image = self.images[self.index]
        self.rect = pygame.Rect(self.x, self.y, 16, 16)

    def update(self):
        self.index += 1
        if self.index >= len(self.images) * 2000:
            self.index = 0
        if self.index % 2000 == 0:
            self.image = self.images[int(self.index/2000)]
        super(TreeSprite, self).update()

# Tree class
class Tree(pygame.sprite.Group):
    def __init__(self, screen, x, y):
        self.screen = screen
        self.tree_sprite = TreeSprite(self.screen, x, y)
        self.x, self.y = self.tree_sprite.x, self.tree_sprite.y
        super(Tree, self).__init__(self.tree_sprite)
