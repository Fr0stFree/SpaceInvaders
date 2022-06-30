import os
import json

import pygame

from .player import Player
from .weapons import Explosion
from .enemies import ExtraEnemy, EnemyGroup


class Game:
    BACKGROUND_IMAGE = pygame.image.load(os.path.join('graphics', 'background.jpg'))
    HEALTH_IMAGE = pygame.image.load(os.path.join('graphics', 'player_ship.png'))
    HEALTH_SIZE = (31, 29)
    FONT_SIZE = 26
    FONT_COLOR = (255, 255, 255)

    def __init__(self, screen, SETTINGS):
        self.SETTINGS = SETTINGS
        self.screen = screen
        self.background_surf = self.BACKGROUND_IMAGE.convert_alpha()
        self.background_rect = self.background_surf.get_rect(topleft=(0, 0))

        self.player = pygame.sprite.GroupSingle(Player(self.SETTINGS))
        self.live_surf = pygame.transform.scale(self.HEALTH_IMAGE.convert_alpha(), self.HEALTH_SIZE)

        self.extra_enemy = pygame.sprite.GroupSingle()

        self.enemies = EnemyGroup(SETTINGS)
        self.enemies.setup()

        self.explosions = pygame.sprite.Group()

        self.score = 0
        self.font = pygame.font.Font(os.path.join('graphics', 'Pixeltype.ttf'), self.FONT_SIZE)

        self.ENEMY_GUNFIRE_EVENT = pygame.USEREVENT + 1
        ENEMY_GUNFIRE_RATE = 300
        pygame.time.set_timer(self.ENEMY_GUNFIRE_EVENT, ENEMY_GUNFIRE_RATE)

    def __str__(self):
        return 'game'

    def display_background(self):
        self.screen.blit(self.background_surf, self.background_rect)

    def display_lives(self):
        for live in range(self.player.sprite.health-1):
            position = (self.SETTINGS['WIDTH'] - (self.HEALTH_SIZE[1] * 2 + 25) + (live * (self.HEALTH_SIZE[1]+10)), 10)
            self.screen.blit(self.live_surf, position)
    
    def display_score(self):
        score_surf = self.font.render(f'score: {self.score}', False, self.FONT_COLOR)
        score_rect = score_surf.get_rect(topleft=(0.05*self.SETTINGS['WIDTH'], 0.95*self.SETTINGS['HEIGHT']))
        self.screen.blit(score_surf, score_rect)

    def projectile_collisions_system(self):
        #  Коллизии ракет игрока
        missiles = self.player.sprite.missiles
        if missiles:
            for missile in missiles:
                #  С обычными противниками
                if pygame.sprite.spritecollide(missile, self.enemies.sprites, True):
                    explosion = Explosion(missile.rect.center)
                    self.explosions.add(explosion)
                    missile.sound_effect.stop()
                    missile.kill()
                    self.score += 1

                #  C Extra Enemy
                if pygame.sprite.spritecollide(missile, self.extra_enemy, False):
                    self.extra_enemy.sprite.health -= 1
                    explosion = Explosion(missile.rect.center)
                    self.explosions.add(explosion)
                    missile.sound_effect.stop()
                    missile.kill()
                    self.score += 5

        # Коллизии лазеров противника
        lasers = self.enemies.lasers
        if lasers:
            for laser in lasers:
                if pygame.sprite.spritecollide(laser, self.player, False):
                    laser.kill()
                    self.player.sprite.health -= 1
                    
        # Коллизии луча специального противника
        if (
            # Должен существовать ExtraEnemy 
            self.extra_enemy
            # Тогда проверим наличие выпущенного им луча
            and self.extra_enemy.sprite.beam.sprite 
            # Тогда проверим коллизию с его прямоугольником
            and pygame.sprite.spritecollide(
                self.extra_enemy.sprite.beam.sprite,
                self.player,
                False,
            )
            # Если коллизия с прямоугольником существует, проверим коллизию с маской
            and pygame.sprite.spritecollide(
                self.extra_enemy.sprite.beam.sprite,
                self.player,
                False,
                pygame.sprite.collide_mask,
            )
        ):
            self.player.sprite.health = 0

    def run(self):
        #  Обновление фона и вспомогательной информации
        self.display_background()
        self.display_score()
        self.display_lives()

        #  Обновление игрока
        if self.player.sprite.health > 0:
            self.player.update()
        else:
            self.player.sprite.explode()
        self.player.draw(self.screen)
        self.player.sprite.missiles.draw(self.screen)

        #  Обновление специального противника
        if self.extra_enemy:
            self.extra_enemy.update()
            # Случай, когда после апдейта Extra Enemy уже удален
            if self.extra_enemy:
                self.extra_enemy.sprite.beam.draw(self.screen)
                self.extra_enemy.draw(self.screen)

        #  Обновление группы противников
        if self.enemies.sprites:
            self.enemies.sprites.update()
            self.enemies.sprites.draw(self.screen)
            self.enemies.movement()
            self.enemies.lasers.update()
            self.enemies.lasers.draw(self.screen)
        elif not self.extra_enemy:
            self.extra_enemy.add(ExtraEnemy(self.SETTINGS))

        #  Отображение взрывов
        if self.explosions:
            self.explosions.draw(self.screen)
            self.explosions.update()

        # Проверка коллизий
        self.projectile_collisions_system()