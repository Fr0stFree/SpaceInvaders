import os
import pygame

import settings


ENEMY_SIZE = (60, 40)


class Enemy(pygame.sprite.Sprite):
    def __init__(self, position):
        super().__init__()
        loaded_image = pygame.image.load(os.path.join('graphics', 'enemy_ship.png')).convert_alpha()
        self.image = pygame.transform.scale(loaded_image, ENEMY_SIZE)
        self.rect = self.image.get_rect(center=position)
