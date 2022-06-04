import os
import pygame

import settings


BEAM_DURATION = 1200
BEAM_SIZE = (125, 800)
BEAM_IMAGE = pygame.image.load(os.path.join('graphics', 'laser_beam.png'))


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
    def __init__(self, position, speed):
        super().__init__()
        self.image = pygame.transform.scale(BEAM_IMAGE.convert_alpha(), BEAM_SIZE)
        self.rect = self.image.get_rect(center=position)
        self.speed = speed
        self.created = pygame.time.get_ticks()
        self.duration = BEAM_DURATION
        
    def update(self):
        self.destroy_sprite()
        self.rect.x += self.speed

    def destroy_sprite(self):
        current_time = pygame.time.get_ticks()
        if current_time - self.created >= self.duration:
            self.kill()

