import os
import pygame

from src.settings import Settings


class Projectile(pygame.sprite.Sprite):
    SPEED = -1
    ACCELERATION = -0.05
    SIZE = (6, 25)
    IMAGE_PATH = pygame.image.load(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'graphics', 'enemy_laser.png'))
    LAUNCH_VOLUME = 0.03

    def __init__(self, position):
        super().__init__()
        self.image = pygame.transform.scale(self.IMAGE_PATH.convert_alpha(), self.SIZE)
        self.rect = self.image.get_rect(center=position)
        self.speed = self.SPEED
        self.acceleration = self.ACCELERATION
        self.sound_effect = pygame.mixer.Sound(os.path.join('audio', 'projectile_launch.mp3'))
        self.sound_effect.play().set_volume(self.LAUNCH_VOLUME)
    
    def destroy_sprite(self):
        if self.rect.y > Settings.HEIGHT or self.rect.y < 0:
            self.kill()

    def update(self):
        self.destroy_sprite()
        self.speed += self.acceleration
        self.rect.y -= self.speed
