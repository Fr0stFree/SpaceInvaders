import sys
import pygame

import settings
from player import Player
from enemy import Enemy

class Game:
    def __init__(self):
        self.player = pygame.sprite.GroupSingle(Player())

        self.enemies = pygame.sprite.Group()
        self.enemies_setup()

    def enemies_setup(self, rows=3, columns=15, x_gap=50, y_gap=50, x_offset=50, y_offset=50):
        for i, row in enumerate(range(rows)):
            for j, column in enumerate(range(columns)):
                position = (j*y_gap+y_offset, i*x_gap+x_offset)
                enemy_sprite = Enemy(position=position)
                self.enemies.add(enemy_sprite)


    def run(self):
        self.player.update()

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