import sys
import pygame

import settings
from player import Player
from enemies import setup_enemies, enemy_movement, enemy_gunfire, ExtraEnemy


ENEMY_GUNFIRE_RATE = 300
EXTRA_ENEMY_APPEARANCE_TIME = 100

class Game:
    def __init__(self):
        self.player = pygame.sprite.GroupSingle(Player())

        self.extra_enemy = pygame.sprite.GroupSingle()
        self.extra_enemy_spawn = EXTRA_ENEMY_APPEARANCE_TIME

        self.enemies = pygame.sprite.Group()
        setup_enemies(self.enemies)
        self.lasers = pygame.sprite.Group()
        
    def extra_enemy_appearance(self):
        if not self.extra_enemy:
            self.extra_enemy_spawn -= 1
        if self.extra_enemy_spawn <= 0:
            self.extra_enemy.add(ExtraEnemy())
            self.extra_enemy_spawn = EXTRA_ENEMY_APPEARANCE_TIME

    def collision_checks(self):
        #  Коллизии ракет игрока
        missiles = self.player.sprite.missiles
        if missiles:
            for missile in missiles:
                if pygame.sprite.spritecollide(missile, self.enemies, True):
                    missile.kill()
                if pygame.sprite.spritecollide(missile, self.extra_enemy, True):
                    missile.kill()
        
        # Коллизии лазеров противника            
        lasers = self.lasers
        if lasers:
            for laser in lasers:
                if pygame.sprite.spritecollide(laser, self.player, True):
                    laser.kill()

        # Коллизии луча специального противника           
        if self.extra_enemy:
            beams = self.extra_enemy.sprite.beams
            if beams:
                for beam in beams:
                    pygame.sprite.spritecollide(beam, self.player, True)


    def run(self):
        #  Обновление игрока
        self.player.update()
        self.player.draw(screen)
        self.player.sprite.missiles.draw(screen)
        
        #  Обновление специального противника
        self.extra_enemy_appearance()
        if self.extra_enemy:
            self.extra_enemy.update()
            self.extra_enemy.sprite.beams.draw(screen)
            self.extra_enemy.draw(screen)

        #  Обновление группы противников
        self.enemies.update()
        self.enemies.draw(screen)
        enemy_movement(self.enemies.sprites())
        self.lasers.update()
        self.lasers.draw(screen)

        # Проверка коллизий
        self.collision_checks()


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