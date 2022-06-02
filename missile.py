import os
import pygame

import settings


MISSILE_SIZE = (10, 45)


class Missile(pygame.sprite.Sprite):
    def __init__(self, position, start_speed, acceleration):
        super().__init__()
        loaded_image = pygame.image.load(os.path.join('graphics', 'player_missile.png')).convert_alpha()
        self.image = pygame.transform.scale(loaded_image, MISSILE_SIZE)
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