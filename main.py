import pygame, sys

import settings
from player import Player

PLAYER_START_POSITION = (settings.WIDTH//2, settings.HEIGHT)

class Game:
    def __init__(self):
        self.player = pygame.sprite.GroupSingle(Player(PLAYER_START_POSITION, 3))

    def run(self):
        self.player.update()
        self.player.draw(screen)  


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