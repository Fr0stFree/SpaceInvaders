import pygame
import os

from .weapons import Missile
from .settings import Settings


class Player(pygame.sprite.Sprite):
    START_HEALTH = 3
    RECOIL_COOLDOWN = 2000
    SPEED = 3
    SIZE = (52,48)
    IMAGE_PATH = pygame.image.load(os.path.join('graphics', 'player_ship.png'))
    EXPLOSIONS_IMAGE = pygame.image.load(os.path.join('graphics', 'explosion.png'))
    EXPLOSION_VOLUME = 0.25
    EXPLOSION_ANIMATION_SPEED = 0.5
    EXPLOSION_RESOLUTION = (2048, 1536)
    EXPLOSION_COLUMNS = 8
    EXPLOSION_ROWS = 6

    def __init__(self):
        super().__init__()
        self.frames = [pygame.transform.scale(self.IMAGE_PATH.convert_alpha(), self.SIZE)]
        self.current_frame = 0
        self.image = self.frames[self.current_frame]
        self.rect = self.image.get_rect(center=(0.5*Settings.WIDTH, 0.9*Settings.HEIGHT))
        self.health = self.START_HEALTH
        self.alive = True
        self.speed = self.SPEED
        self.guns_ready = True
        self.recoil_time = 0
        self.recoil_cooldown = self.RECOIL_COOLDOWN
        self.missiles = pygame.sprite.Group()

        width = self.EXPLOSION_RESOLUTION[0]//self.EXPLOSION_COLUMNS
        height = self.EXPLOSION_RESOLUTION[1]//self.EXPLOSION_ROWS
        for i in range(self.EXPLOSION_ROWS):
            for j in range(self.EXPLOSION_COLUMNS):
                explosion_frame = self.EXPLOSIONS_IMAGE.subsurface((width*j, height*i, width, height)).convert_alpha()
                scaled_explosion_frame = pygame.transform.scale(explosion_frame, (width//2, height//2))
                self.frames.append(scaled_explosion_frame)

    def explode(self):
        try:
            if self.current_frame == 0:
                sound_effect = pygame.mixer.Sound(os.path.join('audio', 'self_explosion.mp3'))
                sound_effect.play().set_volume(self.EXPLOSION_VOLUME)
            self.current_frame += self.EXPLOSION_ANIMATION_SPEED
            self.image = self.frames[int(self.current_frame)]
            self.rect = self.image.get_rect(center=self.rect.center)
        except IndexError:
            self.alive = False

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
        self.missiles.add(Missile(position=self.rect.center))

    def constraint(self):
        if self.rect.right >= Settings.WIDTH:
            self.rect.right = Settings.WIDTH
        if self.rect.left <= 0:
            self.rect.left = 0
        if self.rect.top <= Settings.HEIGHT // 2:
            self.rect.top = Settings.HEIGHT // 2
        if self.rect.bottom >= Settings.HEIGHT:
            self.rect.bottom = Settings.HEIGHT

    def update(self):
        self.get_input()
        self.constraint()
        self.recoil()
        self.missiles.update()
