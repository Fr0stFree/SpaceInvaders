import pygame
import os

import settings 


class Player(pygame.sprite.Sprite):
    def __init__(self, position, speed):
        super().__init__()
        loaded_image = pygame.image.load(os.path.join('graphics', 'player_ship.png')).convert_alpha()
        self.image = pygame.transform.scale(loaded_image, (46, 26))
        self.rect = self.image.get_rect(midbottom=position)
        self.speed = speed

    def get_input(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_RIGHT] and self.rect.right < settings.WIDTH:
            self.rect.x += self.speed
        if keys[pygame.K_LEFT] and self.rect.left > 0:
            self.rect.x -= self.speed
        if keys[pygame.K_UP] and self.rect.top > settings.HEIGHT * 2 // 3:
            self.rect.y -= self.speed + 1
        if keys[pygame.K_DOWN] and self.rect.bottom < settings.HEIGHT:
            self.rect.y += self.speed - 1

    def update(self):
        self.get_input()