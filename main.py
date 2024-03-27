import sys
from typing import Union

import pygame

from src.game import Game
from src.menu import Menu
from src.settings import Settings
from src import music

GameStates = Union[Game, Menu]


if __name__ == '__main__':
    pygame.init()

    screen = pygame.display.set_mode((Settings.WIDTH, Settings.HEIGHT))
    menu = Menu(screen, message='')
    state: GameStates = menu
    clock = pygame.time.Clock()
    music.play()

    while True:
        state.run()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if isinstance(state, Game):
                if event.type == state.ENEMY_GUNFIRE_EVENT:
                    state.enemies.gunfire()

                if not state.player.sprite.alive:
                    message = f'You have lost! Your score: {state.score}'
                    menu = Menu(screen, message)
                    state = menu

                elif state.extra_enemy and not state.extra_enemy.sprite.alive:
                    message = f'You have won! Your score: {state.score}'
                    menu = Menu(screen, message)
                    state = menu

            elif isinstance(state, Menu):
                if state.button_exit.click():
                    pygame.quit()
                    sys.exit()

                if state.button_run.click():
                    state = Game(screen)

        pygame.display.flip()
        clock.tick(Settings.FPS)
