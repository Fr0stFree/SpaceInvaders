import sys
import os
import json

import pygame

from core.game import Game
from core.menu import Menu
from core.settings import Settings


with open('settings.json', 'r') as data:
    SETTINGS = json.load(data)


def play_soundtrack():
    soundtrack = pygame.mixer.Sound(os.path.join('audio', 'Noisia_dustup.mp3'))
    soundtrack.play(loops=-1)
    soundtrack.set_volume(SETTINGS['SOUNDTRACK_VOLUME'])

if __name__ == '__main__':
    pygame.init()
    screen = pygame.display.set_mode((SETTINGS['WIDTH'], SETTINGS['HEIGHT']))
    play_soundtrack()
    clock = pygame.time.Clock()
    menu = Menu(screen)
    procedure = menu

    ENEMY_GUNFIRE_EVENT = pygame.USEREVENT + 1
    ENEMY_GUNFIRE_RATE = 300
    pygame.time.set_timer(ENEMY_GUNFIRE_EVENT, ENEMY_GUNFIRE_RATE)

    while True:
        procedure.run()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if str(procedure) == 'game':
                if event.type == ENEMY_GUNFIRE_EVENT:
                    game.enemies.gunfire()
                
                if not game.player.sprite.alive:
                    menu = Menu(screen, score=game.score)
                    procedure = menu

            elif str(procedure) == 'menu':
                if menu.button_exit.click():
                    pygame.quit()
                    sys.exit()

                if menu.button_run.click():
                    game = Game(screen)
                    procedure = game

                if menu.button_settings.click():
                    pygame.quit()
                    settings = Settings()
                    settings.run()

        pygame.display.flip()
        clock.tick(SETTINGS['FPS'])