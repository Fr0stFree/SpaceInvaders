import sys
from typing import Union

import pygame

from core.game import Game
from core.menu import Menu
from core.settings import Settings
from core.utils import play_music

GameStates = Union[Game, Menu]


if __name__ == '__main__':
    pygame.init()

    screen = pygame.display.set_mode((Settings.WIDTH, Settings.HEIGHT))
    menu = Menu(screen, message='')
    state: GameStates = menu
    clock = pygame.time.Clock()
    play_music()

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
