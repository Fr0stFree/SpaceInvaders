import os
import pygame
import json


class Projectile(pygame.sprite.Sprite):
    SPEED = -1
    ACCELERATION = -0.05
    SIZE = (6, 25)
    IMAGE_PATH = pygame.image.load(os.path.join('graphics', 'enemy_laser.png'))
    LAUNCH_VOLUME = 0.03

    def __init__(self, position, SETTINGS):
        super().__init__()
        self.SETTINGS = SETTINGS
        self.image = pygame.transform.scale(self.IMAGE_PATH.convert_alpha(), self.SIZE)
        self.rect = self.image.get_rect(center=position)
        self.speed = self.SPEED
        self.acceleration = self.ACCELERATION
        self.sound_effect = pygame.mixer.Sound(os.path.join('audio', 'projectile_launch.mp3'))
        self.sound_effect.play().set_volume(self.LAUNCH_VOLUME)
    
    def destroy_sprite(self):
        if self.rect.y > self.SETTINGS['HEIGHT'] or self.rect.y < 0:
            self.kill()

    def update(self):
        self.destroy_sprite()
        self.speed += self.acceleration
        self.rect.y -= self.speed

class Missile(pygame.sprite.Sprite):
    ANIMATION_SPEED = 0.5
    NUMBER_OF_FRAMES = 10
    START_SPEED = 1
    SIZE = (18, 65)
    ACCELERATION = 0.15
    MISSILE_LAUNCH_VOLUME = 0.06

    def __init__(self, position, settings):
        super().__init__()
        self.SETTINGS = settings
        self.frames = []
        for i in range(self.NUMBER_OF_FRAMES):
            missile = pygame.image.load(os.path.join('graphics', 'Missile', f'Missile_3_Flying_00{i}.png')).convert_alpha()
            self.frames.append(pygame.transform.scale(missile, self.SIZE))
        self.current_frame = 0
        self.image = self.frames[self.current_frame]
        self.rect = self.image.get_rect(center=position)
        self.speed = self.START_SPEED
        self.sound_effect = pygame.mixer.Sound(os.path.join('audio', 'missile_launch.mp3'))
        self.sound_effect.play().set_volume(self.MISSILE_LAUNCH_VOLUME)


    def destroy_sprite(self):
        if self.rect.y > self.SETTINGS['HEIGHT'] or self.rect.y < 0:
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
            explosion = pygame.image.load(os.path.join('graphics', 'Missile', f'Missile_3_Explosion_00{i}.png'))
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


class Beam(pygame.sprite.Sprite):
    BEAM_DURATION = 1200
    BEAM_SIZE = (125, 800)
    BEAM_IMAGE = pygame.image.load(os.path.join('graphics', 'laser_beam.png'))
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

