# -*- coding: utf-8 -*-

import time
from core.level_generator import *

#Level - main game logic class
class Level():
    def __init__(self, world, num):
        self.world = world
        self.num = num
        self.ui = pygame.font.SysFont("monaco", 24)
        self.world.pygame.mouse.set_pos(320, 320)
        self.map = self.world.pygame.image.load("./images/levels/level{}.png".format(self.num)).convert()
        self.scoreboard = self.world.pygame.image.load("./images/levels/scoreboard.png").convert()
        self.sound_win = pygame.mixer.Sound("./sounds/level/win.ogg")
        self.generator = LevelGenerator(self.num, self.world)
        self.game_over, self.game_over_font = False, pygame.font.SysFont("monaco", 32)
        self.stars = self.generator.generate_stars()
        self.trees = self.generator.generate_trees()
        self.enemies = self.generator.generate_enemies()
        self.hero = Hero(self.world, self.generator.start_point()[0], self.generator.start_point()[1], 3)

    def draw(self):
        self.world.screen.blit(self.map, [0, 0])
        self.world.screen.blit(self.scoreboard, [0, 0])
        ui_level = self.ui.render("LEVEL {}".format(int(self.num)), 3, (255, 255, 255))
        ui_game_over = self.game_over_font.render("GAME OVER", 5, (255, 255, 255))
        self.world.screen.blit(ui_level, [280, 5])
        if self.game_over:
            self.world.screen.blit(ui_game_over, [220, 320])
        for tree in self.trees:
            tree.draw(self.world.screen)
        for star in self.stars:
            star.draw()
        for enemy in self.enemies:
            enemy.draw(self.world.screen)
        self.hero.drawing()
        self.hero.draw(self.world.screen)

    def update(self):
        for enemy in self.enemies:
            enemy.update()
        for tree in self.trees:
            tree.update()
        self.hero.update()
        if self.stars == []:
            self.go_next_level()

    def go_next_level(self):
        if self.num <= 1:
            self.sound_win.play()
            self.num += 1
            self.__init__(self.world, self.num)
