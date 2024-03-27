import os
from random import choice

import pygame

from src.settings import Settings
from .weapon import Beam


class ExtraEnemy(pygame.sprite.Sprite):
    IMAGE_PATH = pygame.image.load(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'graphics', 'extra_enemy.png'))
    SIZE = (68, 32)
    SPEED = 2
    BEAM_RECOIL_TIME = 3500
    HEALTH = 5

    def __init__(self):
        super().__init__()
        self.image = pygame.transform.scale(self.IMAGE_PATH.convert_alpha(), self.SIZE)
        self.rect = self.image.get_rect(center=choice([
            (-0.05 * Settings.WIDTH, 0.05 * Settings.HEIGHT),
            (1.05 * Settings.WIDTH, 0.05 * Settings.HEIGHT),
        ]))
        self.health = self.HEALTH
        self.speed = self.SPEED
        self.guns_ready = False
        self.recoil_time = 0
        self.beam_reload = self.BEAM_RECOIL_TIME
        self.beam = pygame.sprite.GroupSingle()

    def update(self):
        if self.alive:
            self.beam.update()
            self.gunfire()
            self.movement()
            self.recoil()

    def movement(self):
        self.rect.x += self.speed
        if self.rect.right > 1.1 * Settings.WIDTH or self.rect.left < -Settings.WIDTH // 10:
            self.speed *= -1

    def gunfire(self):
        if self.guns_ready:
            self.beam.add(Beam(position=(self.rect.centerx, self.rect.centery + 400), speed=self.speed))
            self.guns_ready = False
            self.recoil_time = pygame.time.get_ticks()

    def recoil(self):
        if not self.guns_ready:
            current_time = pygame.time.get_ticks()
            if current_time - self.recoil_time >= self.beam_reload:
                self.guns_ready = True

    @property
    def alive(self):
        return self.health > 0
