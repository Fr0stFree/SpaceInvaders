import pygame, sys
from player import Player


FPS = 60
WIDTH = 800
HEIGHT = 600
SCREEN_COLOR = (30, 30, 30)


class Game:
    def __init__(self):
        player_sprite = Player((WIDTH//2, HEIGHT))
        self.player = pygame.sprite.GroupSingle(player_sprite)

    def run(self):
        self.player.update()
        self.player.draw(screen)


if __name__ == '__main__':
    pygame.init()
    screen = pygame.display.set_mode(WIDTH, HEIGHT)
    clock = pygame.time.Clock()
    game = Game()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        screen.fill(SCREEN_COLOR)
        game.run()

        pygame.display.flip()
        clock.tick(FPS)