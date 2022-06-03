import sys
import pygame

import settings
from player import Player
from enemy import setup_enemies, change_enemy_direction

class Game:
    def __init__(self):
        self.player = pygame.sprite.GroupSingle(Player())

        self.enemies = pygame.sprite.Group()
        setup_enemies(self.enemies)


    def run(self):
        self.player.update()

        self.enemies.update()
        change_enemy_direction(self.enemies)

        self.player.draw(screen)
        self.player.sprite.missiles.draw(screen)
        self.enemies.draw(screen)

if __name__ == '__main__':
    pygame.init()
    screen = pygame.display.set_mode((settings.WIDTH, settings.HEIGHT))
    clock = pygame.time.Clock()
    game = Game()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        screen.fill(settings.SCREEN_COLOR)
        game.run()

        pygame.display.flip()
        clock.tick(settings.FPS)