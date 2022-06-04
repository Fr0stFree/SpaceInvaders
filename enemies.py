import os
import pygame
from random import choice

from weapons import Projectile, Beam
import settings


ENEMY_IMAGE = pygame.image.load(os.path.join('graphics', 'enemy_ship.png'))
ENEMY_SIZE = (60, 40)
ENEMY_X_SPEED = 1
ENEMY_Y_SPEED = 0
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

EXTRA_ENEMY_IMAGE = pygame.image.load(os.path.join('graphics', 'extra_enemy.png'))
EXTRA_ENEMY_SIZE = (68, 32)
EXTRA_ENEMY_SPEED = 3
BEAM_RECOIL_TIME = 3500
EXTRA_ENEMY_START_POSITION = choice([
    (-settings.WIDTH//20, settings.HEIGHT//20),
    (1.05*settings.WIDTH, settings.HEIGHT//20),
])


class ExtraEnemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.transform.scale(EXTRA_ENEMY_IMAGE.convert_alpha(), EXTRA_ENEMY_SIZE)
        self.rect = self.image.get_rect(center=EXTRA_ENEMY_START_POSITION)
        self.speed = EXTRA_ENEMY_SPEED 
        
        self.guns_ready = False
        self.recoil_time = 0
        self.beam_reload = BEAM_RECOIL_TIME
        self.beam = pygame.sprite.GroupSingle()

    def update(self):
        self.beam.update()
        self.gunfire()
        self.movement()
        self.recoil()

    def movement(self):
        self.rect.x += self.speed
        if self.rect.right > 1.1*settings.WIDTH or self.rect.left < -settings.WIDTH//10:
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
    

class Enemy(pygame.sprite.Sprite):
    def __init__(self, position):
        super().__init__()
        self.image = pygame.transform.scale(ENEMY_IMAGE.convert_alpha(), ENEMY_SIZE)
        self.rect = self.image.get_rect(center=position)
        self.xspeed = ENEMY_X_SPEED
        self.yspeed = ENEMY_Y_SPEED

    def update(self):
        self.rect.x += self.xspeed
        self.rect.y += self.yspeed

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
        if enemy.rect.left <= 0:
            for enemy in enemies:
                enemy.xspeed = 1
        if enemy.rect.right >= settings.WIDTH:
            for enemy in enemies:
                enemy.xspeed = -1
                

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