import sys
import pygame

import settings
from player import Player
from enemy import setup_enemies, enemy_movement, enemy_gunfire


ENEMY_GUNFIRE_RATE = 300


class Game:
    def __init__(self):
        self.player = pygame.sprite.GroupSingle(Player())

        self.enemies = pygame.sprite.Group()
        setup_enemies(self.enemies)
        self.lasers = pygame.sprite.Group()


    def run(self):
        self.player.update()

        self.enemies.update()
        enemy_movement(self.enemies.sprites())
        self.lasers.update()

        self.player.draw(screen)
        self.player.sprite.missiles.draw(screen)
        self.enemies.draw(screen)
        self.lasers.draw(screen)


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