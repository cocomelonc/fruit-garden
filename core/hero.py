# -*- coding: utf-8 -*-
import pygame
import math
import datetime
import time
from core.weapon import *

# hero class - player
class HeroSprite(pygame.sprite.Sprite):
    def __init__(self, screen, x, y):
        super(HeroSprite, self).__init__()
        self.screen = screen
        self.left, self.right, self.up, self.down = [], [], [], []
        for i in range(9):
            self.left.append(pygame.image.load("./images/hero/hero-left_{}.png".format(i+1)))
            self.right.append(pygame.image.load("./images/hero/hero-right_{}.png".format(i+1)))
            self.down.append(pygame.image.load("./images/hero/hero-down_{}.png".format(i+1)))
            self.up.append(pygame.image.load("./images/hero/hero-up_{}.png".format(i+1)))

        self.attack_img = ()
        for i in ['left', 'right', 'up', 'down']:
            self.attack_img += (pygame.image.load("./images/hero/hero-attack-{}.png".format(i)),)
        self.index = 0
        self.image = self.right[self.index]
        self.x, self.y, self.face = x, y, 'right'
        self.rect = pygame.Rect(self.x, self.y, 16, 16)

    def attack(self):
        if self.face == 'left':
            self.image = self.attack_img[0]
        elif self.face == 'right':
            self.image = self.attack_img[1]
        elif self.face == 'up':
            self.image = self.attack_img[2]
        elif self.face == 'down':
            self.image = self.attack_img[3]

    def move_left(self):
        self.face = 'left'
        self.index += 1
        if self.index >= len(self.left):
            self.index = 0
        self.image = self.left[self.index]
        self.rect = pygame.Rect(self.x - 0.25, self.y, 16, 16)
        self.x -= 0.25

    def move_right(self):
        self.face = 'right'
        self.index += 1
        if self.index >= len(self.right):
            self.index = 0
        self.image = self.right[self.index]
        self.rect = pygame.Rect(self.x + 0.25, self.y, 16, 16)
        self.x += 0.25

    def move_down(self):
        self.face = 'down'
        self.index += 1
        if self.index >= len(self.down):
            self.index = 0
        self.image = self.down[self.index]
        self.rect = pygame.Rect(self.x, self.y + 0.25, 16, 16)
        self.y += 0.25

    def move_up(self):
        self.face = 'up'
        self.index += 1
        if self.index >= len(self.up):
            self.index = 0
        self.image = self.up[self.index]
        self.rect = pygame.Rect(self.x, self.y - 0.25, 16, 16)
        self.y -= 0.25

    def update(self):
        super(HeroSprite, self).update()

class Hero(pygame.sprite.Group):
    def __init__(self, world, x, y, lives):
        self.world = world
        self.screen = self.world.screen
        self.hero_sprite = HeroSprite(self.screen, x, y)
        self.x, self.y = self.hero_sprite.x, self.hero_sprite.y
        self.face, self.centerx, self.centery = 'right', self.hero_sprite.rect.centerx, self.hero_sprite.rect.centery
        self.heart_img = pygame.image.load('./images/hero/heart.png')
        self.star_img = pygame.image.load('./images/hero/star.png')
        self.enemy_img = pygame.image.load("./images/enemies/enemy-down_3.png")
        self.sound_collect = pygame.mixer.Sound("./sounds/hero/collect.ogg")
        self.sound_kill_enemy = pygame.mixer.Sound("./sounds/hero/kill_enemy.ogg")
        self.sound_die = pygame.mixer.Sound("./sounds/hero/die.ogg")
        self.sound_game_over = pygame.mixer.Sound("./sounds/level/game_over.ogg")
        self.sound_collect.set_volume(0.025)
        self.sound_kill_enemy.set_volume(0.025)
        self.lives, self.stars, self.enemy_score, self.stamina = lives, 0, 0, 100
        self.weapon = Weapon(self.screen, self)
        self.ui = pygame.font.SysFont("monaco", 15)
        self.ui_score = pygame.font.SysFont("monaco", 24)
        super(Hero, self).__init__(self.hero_sprite)

    def drawing(self):
        if self.lives > 0:
            for i in range(self.lives):
                self.screen.blit(self.heart_img, [620-(i*20), 4])
        self.screen.blit(self.star_img, [540, 3])
        self.screen.blit(self.enemy_img, [484, 0])
        ui_stars_score = self.ui_score.render("{}".format(int(self.stars)), 3, (255, 255, 255))
        ui_enemy_score = self.ui_score.render("{}".format(int(self.enemy_score)), 3, (255, 255, 255))
        self.screen.blit(ui_stars_score, [558, 4])
        self.screen.blit(ui_enemy_score, [520, 4])
        self.weapon.draw()
        cyear = datetime.datetime.now().year
        copyright = self.ui.render("Copyright (c) %s by zhzhussupovkz" % cyear, 3, (255, 255, 255))
        self.screen.blit(copyright, [240, 620])

    def update(self):
        if self.lives > 0:
            self.face = self.hero_sprite.face
            self.x, self.y = self.hero_sprite.x, self.hero_sprite.y
            self.centerx, self.centery = self.hero_sprite.rect.centerx, self.hero_sprite.rect.centery
            key = pygame.key.get_pressed()
            if key[pygame.K_SPACE]:
                self.attack()
            self.weapon.update()
            self.walk_on_horizontal_roads()
            self.walk_on_vertical_roads()
            self.collect_stars()
            self.add_injury_to_enemies()
        else:
            self.world.level.game_over = True
            self.sound_game_over.play()
            self.world.pause = True
        super(Hero, self).update()

    def move_left(self):
        self.hero_sprite.move_left()

    def move_right(self):
        self.hero_sprite.move_right()

    def move_down(self):
        self.hero_sprite.move_down()

    def move_up(self):
        self.hero_sprite.move_up()

    def walk_on_horizontal_roads(self):
        key = pygame.key.get_pressed()
        if self.world.level.num == 1:
            if (self.x >= 48 and self.x <= 570 and self.y >= 264 and self.y <= 274):
                if key[pygame.K_RIGHT]:
                    if self.x <= 566:
                        self.move_right()
                elif key[pygame.K_LEFT]:
                    if self.x >= 49:
                        self.move_left()
                elif key[pygame.K_UP]:
                    if self.y >= 266:
                        self.move_up()
                elif key[pygame.K_DOWN]:
                    if self.y <= 271:
                        self.move_down()
            if (self.x >= 262 and self.x <= 577 and self.y >= 396 and self.y <= 402):
                if key[pygame.K_RIGHT]:
                    if self.x <= 572:
                        self.move_right()
                elif key[pygame.K_LEFT]:
                    if self.x >= 264:
                        self.move_left()
                elif key[pygame.K_UP]:
                    if self.y >= 397:
                        self.move_up()
                elif key[pygame.K_DOWN]:
                    if self.y <= 399:
                        self.move_down()
            if (self.x >= 266 and self.x <= 600 and self.y >= 556 and self.y <= 560):
                if key[pygame.K_RIGHT]:
                    if self.x <= 598:
                        self.move_right()
                elif key[pygame.K_LEFT]:
                    if self.x >= 268:
                        self.move_left()
                elif key[pygame.K_UP]:
                    if self.y >= 557:
                        self.move_up()
                elif key[pygame.K_DOWN]:
                    if self.y <= 559:
                        self.move_down()
        if self.world.level.num == 2:
            if (self.x >= 24 and self.x <= 570 and self.y >= 58 and self.y <= 66):
                if key[pygame.K_RIGHT]:
                    if self.x <= 566:
                        self.move_right()
                elif key[pygame.K_LEFT]:
                    if self.x >= 25:
                        self.move_left()
                elif key[pygame.K_UP]:
                    if self.y >= 60:
                        self.move_up()
                elif key[pygame.K_DOWN]:
                    if self.y <= 63:
                        self.move_down()
            if (self.x >= 104 and self.x <= 573 and self.y >= 524 and self.y <= 530):
                if key[pygame.K_RIGHT]:
                    if self.x <= 569:
                        self.move_right()
                elif key[pygame.K_LEFT]:
                    if self.x >= 105:
                        self.move_left()
                elif key[pygame.K_UP]:
                    if self.y >= 526:
                        self.move_up()
                elif key[pygame.K_DOWN]:
                    if self.y <= 528:
                        self.move_down()
            if (self.x >= 568 and self.x <= 620 and self.y >= 570 and self.y <= 573):
                if key[pygame.K_RIGHT]:
                    if self.x <= 616:
                        self.move_right()
                elif key[pygame.K_LEFT]:
                    if self.x >= 570:
                        self.move_left()
                elif key[pygame.K_UP]:
                    if self.y >= 571:
                        self.move_up()
                elif key[pygame.K_DOWN]:
                    if self.y <= 572:
                        self.move_down()
            if (self.x >= 44 and self.x <= 104 and self.y >= 460 and self.y <= 464):
                if key[pygame.K_RIGHT]:
                    if self.x <= 103:
                        self.move_right()
                elif key[pygame.K_LEFT]:
                    if self.x >= 45:
                        self.move_left()
                elif key[pygame.K_UP]:
                    if self.y >= 461:
                        self.move_up()
                elif key[pygame.K_DOWN]:
                    if self.y <= 463:
                        self.move_down()

    def walk_on_vertical_roads(self):
        key = pygame.key.get_pressed()
        if self.world.level.num == 1:
            if (self.x >= 566 and self.x <= 575 and self.y >= 270 and self.y <= 400):
                if key[pygame.K_RIGHT]:
                    if self.x <= 570:
                        self.move_right()
                elif key[pygame.K_LEFT]:
                    if self.x >= 569:
                        self.move_left()
                elif key[pygame.K_UP]:
                    if self.y >= 271:
                        self.move_up()
                elif key[pygame.K_DOWN]:
                    if self.y <= 396:
                        self.move_down()
            if (self.x >= 262 and self.x <= 269 and self.y >= 398 and self.y <= 560):
                if key[pygame.K_RIGHT]:
                    if self.x <= 266:
                        self.move_right()
                elif key[pygame.K_LEFT]:
                    if self.x >= 263:
                        self.move_left()
                elif key[pygame.K_UP]:
                    if self.y >= 399:
                        self.move_up()
                elif key[pygame.K_DOWN]:
                    if self.y <= 557:
                        self.move_down()
        elif self.world.level.num == 2:
            if (self.x >= 103 and self.x <= 106 and self.y >= 62 and self.y <= 532):
                if key[pygame.K_RIGHT]:
                    if self.x <= 105:
                        self.move_right()
                elif key[pygame.K_LEFT]:
                    if self.x >= 104:
                        self.move_left()
                elif key[pygame.K_UP]:
                    if self.y >= 63:
                        self.move_up()
                elif key[pygame.K_DOWN]:
                    if self.y <= 528:
                        self.move_down()
            if (self.x >= 566 and self.x <= 570 and self.y >= 61 and self.y <= 575):
                if key[pygame.K_RIGHT]:
                    if self.x <= 569:
                        self.move_right()
                elif key[pygame.K_LEFT]:
                    if self.x >= 567:
                        self.move_left()
                elif key[pygame.K_UP]:
                    if self.y >= 62:
                        self.move_up()
                elif key[pygame.K_DOWN]:
                    if self.y <= 571:
                        self.move_down()

    # attack by weapon
    def attack(self):
        self.hero_sprite.attack()
        self.weapon.drawing = True

    # add injury to enemies
    def add_injury_to_enemies(self):
        if self.weapon.drawing == True:
            for enemy in self.world.level.enemies:
                d = math.sqrt((self.weapon.centerx - enemy.centerx)**2 + (self.weapon.centery - enemy.centery)**2)
                if d <= 4:
                    self.weapon.drawing = False
                    self.sound_kill_enemy.play()
                    self.world.level.enemies.pop(self.world.level.enemies.index(enemy))
                    self.enemy_score += 1
        else:
            for enemy in self.world.level.enemies:
                d_hero = math.sqrt((self.centerx - enemy.centerx)**2 + (self.centery - enemy.centery)**2)
                d_hero_fire = math.sqrt((self.centerx - enemy.weapon.centerx)**2 + (self.centery - enemy.weapon.centery)**2)
                d_weapons = math.sqrt((self.weapon.centerx - enemy.weapon.centerx)**2 + (self.weapon.centery - enemy.weapon.centery)**2)
                if d_hero <= 25:
                    self.add_injury()
                if d_hero_fire <= 25:
                    self.add_injury()
                if d_weapons <= 20:
                    self.weapon.drawing = False
                    enemy.weapon.drawing = False
                if self.hero_see_enemy(enemy):
                    enemy.attack()
                else:
                    enemy.weapon.drawing = False

    def hero_see_enemy(self, enemy):
        if enemy.face == 'left':
            dx = enemy.centerx - self.centerx
            dy = abs(self.centery - enemy.centery)
            if dx > 0 and dx < 128 and dy <= 20:
                return True
        elif enemy.face == 'right':
            dx = self.centerx - enemy.centerx
            dy = abs(self.centery - enemy.centery)
            if dx > 0 and dx < 128 and dy <= 20:
                return True
        elif enemy.face == 'up':
            dx = abs(self.centerx - enemy.centerx)
            dy = enemy.centery - self.centery
            if dy > 0 and dy < 128 and dx <= 20:
                return True
        elif enemy.face == 'down':
            dx = abs(self.centerx - enemy.centerx)
            dy = self.centery - enemy.centery
            if dy > 0 and dy < 128 and dx <= 20:
                return True
        return False

    # collect stars
    def collect_stars(self):
        for star in self.world.level.stars:
            d = math.sqrt((self.centerx - star.x)**2 + (self.centery - star.y)**2)
            if d <= 16:
                self.sound_collect.play()
                self.world.level.stars.pop(self.world.level.stars.index(star))
                self.stars += 1

    # add injury when enemies attack hero
    def add_injury(self):
        if self.face == 'left':
            self.x += 8
        elif self.face == 'right':
            self.x -= 8
        elif self.face == 'up':
            self.y += 8
        elif self.face == 'down':
            self.y -= 8
        self.stamina -= 10
        if self.stamina <= 0:
            if self.lives > 0:
                self.sound_die.play()
                time.sleep(3)
                self.stamina = 0
                self.reboot()

    # reboot hero if die
    def reboot(self):
        self.lives -= 1
        start_x = self.world.level.generator.start_point()[0]
        start_y = self.world.level.generator.start_point()[1]
        self.__init__(self.world, start_x, start_y, self.lives)
