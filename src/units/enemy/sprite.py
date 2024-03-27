import os
from random import choice

import pygame

from src.settings import Settings
from .weapon import Projectile



class Enemy(pygame.sprite.Sprite):
    IMAGE_PATH = pygame.image.load(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'graphics', 'enemy_ship.png'))
    SIZE = (35, 34)
    SPEED = 1

    def __init__(self, position):
        super().__init__()
        self.image = pygame.transform.scale(self.IMAGE_PATH.convert_alpha(), self.SIZE)
        self.rect = self.image.get_rect(center=position)
        self.xspeed = self.SPEED

    def update(self):
        self.rect.x += self.xspeed


class EnemyGroup:
    X_GAP = 85
    Y_GAP = 70
    X_OFFSET = 50
    Y_OFFSET = 75
    ROWS = 3
    COLUMNS = 7

    def __init__(self):
        self.sprites = pygame.sprite.Group()
        self.lasers = pygame.sprite.Group()

    def setup(self):
        for i, row in enumerate(range(self.ROWS)):
            for j, column in enumerate(range(self.COLUMNS)):
                position = (
                    j * self.X_GAP + self.X_OFFSET,
                    i * self.Y_GAP + self.Y_OFFSET,
                )
                enemy_sprite = Enemy(position=position)
                self.sprites.add(enemy_sprite)

    def movement(self):
        for enemy in self.sprites:
            if enemy.rect.left <= 0:
                for enemy in self.sprites:
                    enemy.xspeed = 1
            if enemy.rect.right >= Settings.WIDTH:
                for enemy in self.sprites:
                    enemy.xspeed = -1

    def gunfire(self):
        if self.sprites:
            random_enemy = choice(list(self.sprites))
            laser_sprite = Projectile(position=random_enemy.rect.center)
            self.lasers.add(laser_sprite)