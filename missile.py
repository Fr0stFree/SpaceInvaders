import os
import pygame


class Missile(pygame.sprite.Sprite):
    def __init__(self, position, speed):
        super().__init__()
        loaded_image = pygame.image.load(os.path.join('graphics', 'player_missile.png')).convert_alpha()
        self.image = pygame.transform.scale(loaded_image, (10, 45))
        self.rect = self.image.get_rect(center=position)
        self.speed = speed
        self.acceleration = 0

    def update(self):
        self.acceleration += 0.15
        self.rect.y -= self.speed + self.acceleration