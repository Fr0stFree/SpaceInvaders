import pygame
import os

import settings
from weapons import Missile


PLAYER_START_POSITION = (settings.WIDTH//2, settings.HEIGHT)
PLAYER_SPEED = 3
PLAYER_SIZE = (52,48)
PLAYER_IMAGE = pygame.image.load(os.path.join('graphics', 'player_ship.png'))

RECOIL_COOLDOWN = 1600


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.transform.scale(PLAYER_IMAGE.convert_alpha(), PLAYER_SIZE)
        self.rect = self.image.get_rect(midbottom=PLAYER_START_POSITION)
        self.speed = PLAYER_SPEED
        self.guns_ready = True
        self.recoil_time = 0
        self.recoil_cooldown = RECOIL_COOLDOWN
        
        self.missiles = pygame.sprite.Group()

    def get_input(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_d]:
            self.rect.x += self.speed
        if keys[pygame.K_a]:
            self.rect.x -= self.speed
        if keys[pygame.K_w]:
            self.rect.y -= self.speed + 1
        if keys[pygame.K_s]:
            self.rect.y += self.speed - 1
        if keys[pygame.K_SPACE] and self.guns_ready:
            self.gunfire()
            self.guns_ready = False
            self.recoil_time = pygame.time.get_ticks()

    def recoil(self):
        if not self.guns_ready:
            current_time = pygame.time.get_ticks()
            if current_time - self.recoil_time >= self.recoil_cooldown:
                self.guns_ready = True

    def gunfire(self):
        self.missiles.add(
            Missile(
                position=self.rect.center,
            )
        )

    def constraint(self):
        if self.rect.right >= settings.WIDTH:
            self.rect.right = settings.WIDTH
        if self.rect.left <= 0:
            self.rect.left = 0
        if self.rect.top <= settings.HEIGHT // 2:
            self.rect.top = settings.HEIGHT // 2
        if self.rect.bottom >= settings.HEIGHT:
            self.rect.bottom = settings.HEIGHT

    def update(self):
        self.get_input()
        self.constraint()
        self.recoil()
        self.missiles.update()