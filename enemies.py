import os
import pygame
from random import choice

from weapons import Projectile, Beam
import settings


ENEMY_SIZE = (60, 40)
ENEMY_SPEED = 1
ENEMY_STEP_SIZE = 5
ENEMY_X_GAP = 65
ENEMY_Y_GAP = 50
ENEMY_X_OFFSET = 50
ENEMY_Y_OFFSET = 75
ENEMY_ROWS = 3
ENEMY_COLUMNS = 10
ENEMY_LASER_SPEED = -1
ENEMY_LASER_ACCELERATION = -0.1
ENEMY_LASER_SIZE = (6, 25)

EXTRA_ENEMY_SIZE = (68, 32)
EXTRA_ENEMY_SPEED = 3
EXTRA_ENEMY_START_POSITION = choice(((-settings.WIDTH//20, settings.HEIGHT//20), (1.05*settings.WIDTH, settings.HEIGHT//20)))
BEAM_RECOIL_TIME = 3500

class ExtraEnemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        loaded_image = pygame.image.load(os.path.join('graphics', 'extra_enemy.png')).convert_alpha()
        self.image = pygame.transform.scale(loaded_image, EXTRA_ENEMY_SIZE)
        self.rect = self.image.get_rect(center=EXTRA_ENEMY_START_POSITION)
        self.speed = EXTRA_ENEMY_SPEED 
        
        self.guns_ready = False
        self.recoil_time = 0
        self.beam_reload = BEAM_RECOIL_TIME
        self.beams = pygame.sprite.Group()

    def update(self):
        self.beams.update()
        self.gunfire()
        self.movement()
        self.recoil()

    def movement(self):
        self.rect.x += self.speed
        if self.rect.right > 1.1*settings.WIDTH or self.rect.left < -settings.WIDTH//10:
            self.speed *= -1

    def gunfire(self):
        if self.guns_ready:
            self.beams.add(
                Beam(
                    path='laser_beam.png',
                    position=(self.rect.centerx, self.rect.centery+200),
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
    laser_sprite = Projectile(
        path='enemy_laser.png',
        position=random_enemy.rect.center,
        start_speed=ENEMY_LASER_SPEED,
        acceleration=ENEMY_LASER_ACCELERATION,
        size=ENEMY_LASER_SIZE,
    )
    lasers.add(laser_sprite)