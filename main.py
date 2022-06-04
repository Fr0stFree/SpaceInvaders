import sys
import os
import pygame

import settings
from player import Player
from enemies import setup_enemies, enemy_movement, enemy_gunfire, ExtraEnemy

BACKGROUND_IMAGE = pygame.image.load(os.path.join('graphics', 'background.jpg'))
HEALTH_SIZE = (31, 29)
HEALTH_IMAGE = pygame.image.load(os.path.join('graphics', 'player_ship.png'))
FONT_SIZE = 26
FONT_COLOR = (255, 255, 255)

ENEMY_GUNFIRE_RATE = 300
EXTRA_ENEMY_APPEARANCE_TIME = 1000

class Game:
    def __init__(self):
        self.background_surf = BACKGROUND_IMAGE.convert_alpha()
        self.background_rect = self.background_surf.get_rect(topleft=(0, 0))
        
        self.player = pygame.sprite.GroupSingle(Player())
        self.lives = 3
        self.live_surf = pygame.transform.scale(HEALTH_IMAGE.convert_alpha(), HEALTH_SIZE)
        
        self.extra_enemy = pygame.sprite.GroupSingle()
        self.extra_enemy_spawn = EXTRA_ENEMY_APPEARANCE_TIME

        self.enemies = pygame.sprite.Group()
        self.lasers = pygame.sprite.Group()
        setup_enemies(self.enemies)
        
        self.score = 0
        self.font = pygame.font.Font(os.path.join('Pixeltype.ttf'), FONT_SIZE)

    def display_background(self):
        screen.blit(self.background_surf, self.background_rect)

    def extra_enemy_appearance(self):
        if len(self.enemies) < 18:
            if not self.extra_enemy:
                self.extra_enemy_spawn -= 1
            if self.extra_enemy_spawn <= 0:
                self.extra_enemy.add(ExtraEnemy())
                self.extra_enemy_spawn = EXTRA_ENEMY_APPEARANCE_TIME

    def player_health_system(self):
        if self.lives <= 0: 
            pygame.quit()
            sys.exit()
        for live in range(self.lives-1):
            position = (settings.WIDTH - (HEALTH_SIZE[1] * 2 + 25) + (live * (HEALTH_SIZE[1]+10)), 10)
            screen.blit(self.live_surf, position)
    
    def score_system(self):
        score_surf = self.font.render(f'score: {self.score}', False, FONT_COLOR)
        score_rect = score_surf.get_rect(topleft=(0.05*settings.WIDTH, 0.95*settings.HEIGHT))
        screen.blit(score_surf, score_rect)

    def projectile_collisions_system(self):
        #  Коллизии ракет игрока
        missiles = self.player.sprite.missiles
        if missiles:
            for missile in missiles:
                if pygame.sprite.spritecollide(missile, self.enemies, True):
                    missile.kill()
                    self.score += 1
                if pygame.sprite.spritecollide(missile, self.extra_enemy, True):
                    missile.kill()
                    self.score += 5
        
        # Коллизии лазеров противника            
        lasers = self.lasers
        if lasers:
            for laser in lasers:
                if pygame.sprite.spritecollide(laser, self.player, False):
                    laser.kill()
                    self.lives -= 1

        # Коллизии луча специального противника        
        if self.extra_enemy:
            beam = self.extra_enemy.sprite.beam.sprite
            if beam:
                if pygame.sprite.spritecollide(beam, self.player, False):
                    beam.kill()
                    self.lives -= 1
        
    def run(self):
        #  Обновление фона
        self.display_background()

        #  Обновление игрока
        self.player.update()
        self.player.draw(screen)
        self.player.sprite.missiles.draw(screen)
        self.player_health_system()
        
        #  Обновление специального противника
        self.extra_enemy_appearance()
        if self.extra_enemy:
            self.extra_enemy.update()
            self.extra_enemy.sprite.beam.draw(screen)
            self.extra_enemy.draw(screen)

        #  Обновление группы противников
        self.enemies.update()
        self.enemies.draw(screen)
        enemy_movement(self.enemies.sprites())
        self.lasers.update()
        self.lasers.draw(screen)

        # Проверка коллизий
        self.projectile_collisions_system()

        # Отображение очков
        self.score_system()


if __name__ == '__main__':
    pygame.init()
    screen = pygame.display.set_mode((settings.WIDTH, settings.HEIGHT))
    clock = pygame.time.Clock()
    game = Game()

    ENEMY_GUNFIRE_EVENT = pygame.USEREVENT + 1
    pygame.time.set_timer(ENEMY_GUNFIRE_EVENT, ENEMY_GUNFIRE_RATE)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            
            if event.type == ENEMY_GUNFIRE_EVENT:
                enemy_gunfire(game.enemies.sprites(), game.lasers)


        screen.fill(settings.SCREEN_COLOR)
        game.run()

        pygame.display.flip()
        clock.tick(settings.FPS)