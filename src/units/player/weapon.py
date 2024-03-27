import os
import pygame

from src.settings import Settings


class Missile(pygame.sprite.Sprite):
    ANIMATION_SPEED = 0.5
    NUMBER_OF_FRAMES = 10
    START_SPEED = 1
    SIZE = (18, 65)
    ACCELERATION = 0.15
    MISSILE_LAUNCH_VOLUME = 0.06

    def __init__(self, position):
        super().__init__()
        self.frames = []
        for i in range(self.NUMBER_OF_FRAMES):
            missile = pygame.image.load(os.path.join(os.path.dirname(__file__), 'graphics', 'Missile', f'Missile_3_Flying_00{i}.png')).convert_alpha()
            self.frames.append(pygame.transform.scale(missile, self.SIZE))
        self.current_frame = 0
        self.image = self.frames[self.current_frame]
        self.rect = self.image.get_rect(center=position)
        self.speed = self.START_SPEED
        self.sound_effect = pygame.mixer.Sound(os.path.join('audio', 'missile_launch.mp3'))
        self.sound_effect.play().set_volume(self.MISSILE_LAUNCH_VOLUME)


    def destroy_sprite(self):
        if self.rect.y > Settings.HEIGHT or self.rect.y < 0:
            self.kill()

    def update(self):
        if self.current_frame < self.NUMBER_OF_FRAMES-1:
            self.current_frame += self.ANIMATION_SPEED
        else:
            self.current_frame = 0
        self.image = self.frames[int(self.current_frame)]
        self.destroy_sprite()
        self.speed += self.ACCELERATION
        self.rect.y -= self.speed


class Explosion(pygame.sprite.Sprite):
    SIZE = (100, 100)
    ANIMATION_SPEED = 1
    NUMBER_OF_FRAMES = 9
    EXPLOSION_VOLUME = 0.33

    def __init__(self, position):
        super().__init__()
        self.frames = []
        for i in range(self.NUMBER_OF_FRAMES):
            explosion = pygame.image.load(os.path.join(os.path.dirname(__file__), 'graphics', 'Missile', f'Missile_3_Explosion_00{i}.png'))
            self.frames.append(pygame.transform.scale(explosion, (self.SIZE)))
        self.current_frame = 0
        self.image = self.frames[self.current_frame]
        self.rect = self.image.get_rect(center=position)
        self.sound_effect = pygame.mixer.Sound(os.path.join('audio', 'missile_explosion.mp3'))
        self.sound_effect.play().set_volume(self.EXPLOSION_VOLUME)

    def update(self):
        try:
            self.current_frame += self.ANIMATION_SPEED
            self.image = self.frames[int(self.current_frame)]
        except IndexError:
            self.kill()
