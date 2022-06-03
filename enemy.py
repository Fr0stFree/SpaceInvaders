import os
import pygame
from random import choice

from laser import Laser
import settings


ENEMY_SIZE = (60, 40)
ENEMY_SPEED = 1
ENEMY_STEP_SIZE = 5
ENEMY_X_GAP = 65
ENEMY_Y_GAP = 50
ENEMY_X_OFFSET = 50
ENEMY_Y_OFFSET = 50
ENEMY_ROWS = 3
ENEMY_COLUMNS = 10

EXTRA_ENEMY_SIZE = ...
EXTRA_ENEMY_SPEED = ...

class Enemy(pygame.sprite.Sprite):
    def __init__(self, position):
        super().__init__()
        loaded_image = pygame.image.load(os.path.join('graphics', 'enemy_ship.png')).convert_alpha()
        self.image = pygame.transform.scale(loaded_image, ENEMY_SIZE)
        self.rect = self.image.get_rect(center=position)
        self.speed = ENEMY_SPEED
        self.step = ENEMY_STEP_SIZE

    def update(self):
        self.rect.x += self.speed


class ExtraEnemy(pygame.sprite.Sprite):
    def __init__(self, position):
        super().__init__()
        loaded_image = ... # pygame.image.load(os.path.join('graphics', 'enemy_ship.png')).convert_alpha()
        self.image = pygame.transform.scale(loaded_image, EXTRA_ENEMY_SIZE)
        self.rect = self.image.get_rect(center=position)
        self.speed = EXTRA_ENEMY_SPEED        


def setup_enemies(group):
    for i, row in enumerate(range(ENEMY_ROWS)):
        for j, column in enumerate(range(ENEMY_COLUMNS)):
            position = (
                j * ENEMY_X_GAP + ENEMY_X_OFFSET,
                i * ENEMY_Y_GAP + ENEMY_Y_OFFSET,
            )
            enemy_sprite = Enemy(position=position)
            group.add(enemy_sprite)

def enemy_movement(enemies):
    for enemy in enemies:
        if enemy.rect.right >= settings.WIDTH or enemy.rect.left <= 0:
            for enemy in enemies:
                enemy.speed *= -1
                enemy.rect.y += enemy.step

def enemy_gunfire(enemies, lasers):
    random_enemy = choice(enemies)
    laser_sprite = Laser(
        position=random_enemy.rect.center,
        start_speed=1,
        acceleration=0.1
    )
    lasers.add(laser_sprite)