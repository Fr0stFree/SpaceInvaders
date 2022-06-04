import os
import pygame

import settings


class Projectile(pygame.sprite.Sprite):
    def __init__(self, path, position, start_speed, acceleration, size):
        super().__init__()
        loaded_image = pygame.image.load(os.path.join('graphics', path)).convert_alpha()
        self.image = pygame.transform.scale(loaded_image, size)
        self.rect = self.image.get_rect(center=position)
        self.speed = start_speed
        self.acceleration = acceleration

    def destroy_sprite(self):
        if self.rect.y > settings.HEIGHT or self.rect.y < 0:
            self.kill()

    def update(self):
        self.destroy_sprite()
        self.speed += self.acceleration
        self.rect.y -= self.speed


class Beam(pygame.sprite.Sprite):
    def __init__(self, path, position, speed):
        super().__init__()
        self.image = pygame.image.load(os.path.join('graphics', path)).convert_alpha()
        self.rect = self.image.get_rect(center=position)
        self.speed = speed
        self.created = pygame.time.get_ticks()
        self.duration = 1200
        
    def update(self):
        self.destroy_sprite()
        self.rect.x += self.speed

    def destroy_sprite(self):
        current_time = pygame.time.get_ticks()
        if current_time - self.created >= self.duration:
            self.kill()

