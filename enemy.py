import os
import pygame

import settings


ENEMY_SIZE = (60, 40)
ENEMY_SPEED = 1

class Enemy(pygame.sprite.Sprite):
    def __init__(self, position):
        super().__init__()
        loaded_image = pygame.image.load(os.path.join('graphics', 'enemy_ship.png')).convert_alpha()
        self.image = pygame.transform.scale(loaded_image, ENEMY_SIZE)
        self.rect = self.image.get_rect(center=position)
        self.speed = ENEMY_SPEED

    def update(self):
        self.rect.x += self.speed


def setup_enemies(group, rows=3, columns=10, x_gap=65, y_gap=50, x_offset=50, y_offset=50):
    for i, row in enumerate(range(rows)):
        for j, column in enumerate(range(columns)):
            position = (j*x_gap+x_offset, i*y_gap+y_offset)
            enemy_sprite = Enemy(position=position)
            group.add(enemy_sprite)

def change_enemy_direction(enemies):
    for enemy in enemies:
        if enemy.rect.right >= settings.WIDTH or enemy.rect.left <= 0:
            for enemy in enemies:
                enemy.speed *= -1