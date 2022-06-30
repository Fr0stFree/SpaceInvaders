import os
from random import choice
import json

import pygame

from .weapons import Projectile, Beam


class ExtraEnemy(pygame.sprite.Sprite):
    IMAGE_PATH = pygame.image.load(os.path.join('graphics', 'extra_enemy.png'))
    SIZE = (68, 32)
    SPEED = 2
    BEAM_RECOIL_TIME = 3500
    HEALTH = 5

    def __init__(self, SETTINGS):
        super().__init__()
        self.SETTINGS = SETTINGS
        self.image = pygame.transform.scale(self.IMAGE_PATH.convert_alpha(), self.SIZE)
        self.rect = self.image.get_rect(center=choice([
            (-0.05*self.SETTINGS['WIDTH'], 0.05*self.SETTINGS['HEIGHT']),
            (1.05*self.SETTINGS['WIDTH'], 0.05*self.SETTINGS['HEIGHT']),
        ]))
        self.health = self.HEALTH
        self.speed = self.SPEED 
        
        self.guns_ready = False
        self.recoil_time = 0
        self.beam_reload = self.BEAM_RECOIL_TIME
        self.beam = pygame.sprite.GroupSingle()

    def update(self):
        self.beam.update()
        self.gunfire()
        self.movement()
        self.recoil()
        self.death()

    def movement(self):
        self.rect.x += self.speed
        if self.rect.right > 1.1*self.SETTINGS['WIDTH'] or self.rect.left < -self.SETTINGS['WIDTH']//10:
            self.speed *= -1

    def gunfire(self):
        if self.guns_ready:
            self.beam.add(
                Beam(
                    position=(self.rect.centerx, self.rect.centery+400),
                    speed=self.speed,
                )
            )
            self.guns_ready = False
            self.recoil_time = pygame.time.get_ticks()
    
    def recoil(self):
        if not self.guns_ready:
            current_time = pygame.time.get_ticks()
            if current_time - self.recoil_time >= self.beam_reload:
                self.guns_ready = True

    def death(self):
        if self.health <= 0:
            self.kill()
    

class Enemy(pygame.sprite.Sprite):
    IMAGE_PATH = pygame.image.load(os.path.join('graphics', 'enemy_ship.png'))
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

    def __init__(self, SETTINGS):
        self.SETTINGS = SETTINGS
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
            if enemy.rect.right >= self.SETTINGS['WIDTH']:
                for enemy in self.sprites:
                    enemy.xspeed = -1

    def gunfire(self):
        if self.sprites:
            random_enemy = choice(list(self.sprites))
            laser_sprite = Projectile(position=random_enemy.rect.center, SETTINGS=self.SETTINGS)
            self.lasers.add(laser_sprite)