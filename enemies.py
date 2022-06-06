import os
import pygame
from random import choice

from weapons import Projectile, Beam
import settings


ENEMY_X_GAP = 85
ENEMY_Y_GAP = 70
ENEMY_X_OFFSET = 50
ENEMY_Y_OFFSET = 75
ENEMY_ROWS = 3
ENEMY_COLUMNS = 7
ENEMY_LASER_SPEED = -1
ENEMY_LASER_ACCELERATION = -0.1
ENEMY_LASER_SIZE = (6, 25)





class ExtraEnemy(pygame.sprite.Sprite):
    EXTRA_ENEMY_IMAGE = pygame.image.load(os.path.join('graphics', 'extra_enemy.png'))
    EXTRA_ENEMY_SIZE = (68, 32)
    EXTRA_ENEMY_SPEED = 2
    BEAM_RECOIL_TIME = 3500
    EXTRA_ENEMY_START_POSITION = choice([
        (-settings.WIDTH//20, settings.HEIGHT//20),
        (1.05*settings.WIDTH, settings.HEIGHT//20),
    ])

    def __init__(self):
        super().__init__()
        self.image = pygame.transform.scale(self.EXTRA_ENEMY_IMAGE.convert_alpha(), self.EXTRA_ENEMY_SIZE)
        self.rect = self.image.get_rect(center=self.EXTRA_ENEMY_START_POSITION)
        self.speed = self.EXTRA_ENEMY_SPEED 
        
        self.guns_ready = False
        self.recoil_time = 0
        self.beam_reload = self.BEAM_RECOIL_TIME
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
    ENEMY_IMAGE = pygame.image.load(os.path.join('graphics', 'enemy_ship.png'))
    ENEMY_SIZE = (35, 34)
    ENEMY_X_SPEED = 1

    def __init__(self, position):
        super().__init__()
        self.image = pygame.transform.scale(self.ENEMY_IMAGE.convert_alpha(), self.ENEMY_SIZE)
        self.rect = self.image.get_rect(center=position)
        self.xspeed = self.ENEMY_X_SPEED

    def update(self):
        self.rect.x += self.xspeed


class Explosion(pygame.sprite.Sprite):
    EXPLOSION_SIZE = (100, 100)
    EXPLOSION_ANIMATION_SPEED = 1.5

    def __init__(self, position):
        super().__init__()
        self.frames = []
        for i in range(9):
            explosion = pygame.image.load(os.path.join('graphics', 'Missile', f'Missile_3_Explosion_00{i}.png'))
            self.frames.append(pygame.transform.scale(explosion, (self.EXPLOSION_SIZE)))
        self.current_frame = 0
        self.image = self.frames[self.current_frame]
        self.rect = self.image.get_rect(center=position)

    def update(self):
        try: 
            self.current_frame += self.EXPLOSION_ANIMATION_SPEED
            self.image = self.frames[int(self.current_frame)]
        except IndexError:
            self.kill()


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
        position=random_enemy.rect.center,
        start_speed=ENEMY_LASER_SPEED,
        acceleration=ENEMY_LASER_ACCELERATION,
        size=ENEMY_LASER_SIZE,
    )
    lasers.add(laser_sprite)