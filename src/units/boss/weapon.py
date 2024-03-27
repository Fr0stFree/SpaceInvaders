import os
import pygame


class Beam(pygame.sprite.Sprite):
    BEAM_DURATION = 1200
    BEAM_SIZE = (125, 800)
    BEAM_IMAGE = pygame.image.load(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'graphics', 'laser_beam.png'))
    BEAM_VOLUME = 0.1

    def __init__(self, position, speed):
        super().__init__()
        self.image = pygame.transform.scale(self.BEAM_IMAGE.convert_alpha(), self.BEAM_SIZE)
        self.rect = self.image.get_rect(center=position)
        self.mask = pygame.mask.from_surface(self.image)
        self.speed = speed
        self.created = pygame.time.get_ticks()
        self.sound_effect = pygame.mixer.Sound(os.path.join('audio', 'laser_beam.mp3'))
        self.sound_effect.play().set_volume(self.BEAM_VOLUME)
        
    def update(self):
        self.destroy_sprite()
        self.rect.x += self.speed

    def destroy_sprite(self):
        current_time = pygame.time.get_ticks()
        if current_time - self.created >= self.BEAM_DURATION:
            self.kill()

