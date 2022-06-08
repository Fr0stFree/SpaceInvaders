import sys
import os
import pygame

import settings
from player import Player
from weapons import Explosion
from enemies import ExtraEnemy, EnemyGroup


BACKGROUND_IMAGE = pygame.image.load(os.path.join('graphics', 'background.jpg'))

class Menu:
    FONT_COLOR = (150, 150, 150)
    FONT_SIZE = 36
    MENU_MESSAGE = 'Press space to run the game'

    def __init__(self, score):
        self.background_surf = BACKGROUND_IMAGE.convert_alpha()
        self.background_rect = self.background_surf.get_rect(topleft=(0, 0))
        self.text_font = pygame.font.Font(os.path.join('graphics', 'Pixeltype.ttf'), self.FONT_SIZE)
        self.text_surf = self.text_font.render(self.MENU_MESSAGE, False, self.FONT_COLOR)
        self.text_rect = self.text_surf.get_rect(center=(0.5*settings.WIDTH, 0.7*settings.HEIGHT))
        self.score = score
    
    def run(self):
        screen.blit(self.background_surf, self.background_rect)
        screen.blit(self.text_surf, self.text_rect)
        if self.score:
            score_surf = self.text_font.render(f'your score: {self.score}', False, self.FONT_COLOR)
            score_rect = score_surf.get_rect(center=(0.5*settings.WIDTH, 0.45*settings.HEIGHT))
            screen.blit(score_surf, score_rect)


class Game:
    HEALTH_IMAGE = pygame.image.load(os.path.join('graphics', 'player_ship.png'))
    HEALTH_SIZE = (31, 29)
    FONT_SIZE = 26
    FONT_COLOR = (255, 255, 255)
    ENEMY_GUNFIRE_RATE = 300
    ENEMIES_BEFORE_THE_BOSS = 12
    EXTRA_ENEMY_APPEARANCE_TIME = 1000

    def __init__(self):
        self.background_surf = BACKGROUND_IMAGE.convert_alpha()
        self.background_rect = self.background_surf.get_rect(topleft=(0, 0))

        self.player = pygame.sprite.GroupSingle(Player())
        self.live_surf = pygame.transform.scale(self.HEALTH_IMAGE.convert_alpha(), self.HEALTH_SIZE)

        self.extra_enemy = pygame.sprite.GroupSingle()
        self.extra_enemy_spawn = self.EXTRA_ENEMY_APPEARANCE_TIME

        self.enemies = EnemyGroup()
        self.enemies.setup()

        self.explosions = pygame.sprite.Group()

        self.score = 0
        self.font = pygame.font.Font(os.path.join('graphics', 'Pixeltype.ttf'), self.FONT_SIZE)

    def display_background(self):
        screen.blit(self.background_surf, self.background_rect)

    def display_lives(self):
        for live in range(self.player.sprite.health-1):
            position = (settings.WIDTH - (self.HEALTH_SIZE[1] * 2 + 25) + (live * (self.HEALTH_SIZE[1]+10)), 10)
            screen.blit(self.live_surf, position)
    
    def display_score(self):
        score_surf = self.font.render(f'score: {self.score}', False, self.FONT_COLOR)
        score_rect = score_surf.get_rect(topleft=(0.05*settings.WIDTH, 0.95*settings.HEIGHT))
        screen.blit(score_surf, score_rect)

    @staticmethod
    def play_music():
        soundtrack = pygame.mixer.Sound(os.path.join('audio', 'Noisia_dustup.mp3'))
        soundtrack.play(loops=-1)
        soundtrack.set_volume(0.25)

    def extra_enemy_appearance(self):
        if len(self.enemies.sprites) < self.ENEMIES_BEFORE_THE_BOSS:
            if not self.extra_enemy:
                self.extra_enemy_spawn -= 1
            if self.extra_enemy_spawn <= 0:
                self.extra_enemy.add(ExtraEnemy())
                self.extra_enemy_spawn = self.EXTRA_ENEMY_APPEARANCE_TIME

    def projectile_collisions_system(self):
        #  Коллизии ракет игрока
        missiles = self.player.sprite.missiles
        if missiles:
            for missile in missiles:
                if pygame.sprite.spritecollide(missile, self.enemies.sprites, True):
                    explosion = Explosion(missile.rect.center)
                    self.explosions.add(explosion)
                    missile.sound_effect.stop()
                    missile.kill()
                    self.score += 1
                if pygame.sprite.spritecollide(missile, self.extra_enemy, True):
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
        if self.extra_enemy:
            beam = self.extra_enemy.sprite.beam.sprite
            if beam:
                if pygame.sprite.spritecollide(beam, self.player, False):
                    self.player.sprite.health -= 1

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

        self.player.draw(screen)
        self.player.sprite.missiles.draw(screen)

        #  Обновление специального противника
        self.extra_enemy_appearance()
        if self.extra_enemy:
            self.extra_enemy.update()
            self.extra_enemy.sprite.beam.draw(screen)
            self.extra_enemy.draw(screen)

        #  Обновление группы противников
        if self.enemies.sprites:
            self.enemies.sprites.update()
            self.enemies.sprites.draw(screen)
            self.enemies.movement()
            self.enemies.lasers.update()
            self.enemies.lasers.draw(screen)
        else:
            self.score += 5
            self.enemies.setup()

        #  Отображение взрывов
        if self.explosions:
            self.explosions.draw(screen)
            self.explosions.update()

        # Проверка коллизий
        self.projectile_collisions_system()


if __name__ == '__main__':
    pygame.init()
    screen = pygame.display.set_mode((settings.WIDTH, settings.HEIGHT))
    clock = pygame.time.Clock()
    game = Game()
    game.play_music()

    ENEMY_GUNFIRE_EVENT = pygame.USEREVENT + 1
    pygame.time.set_timer(ENEMY_GUNFIRE_EVENT, game.ENEMY_GUNFIRE_RATE)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == ENEMY_GUNFIRE_EVENT:
                game.enemies.gunfire()

            #  Перезапуск игры
            if not game.player.sprite.alive:
                if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                    game = Game()

        if game.player.sprite.alive:
            game.run()
        else:
            game.enemies.sprites.empty()
            menu = Menu(game.score)
            menu.run()

        pygame.display.flip()
        clock.tick(settings.FPS)