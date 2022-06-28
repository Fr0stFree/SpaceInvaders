import sys
import os
import json

import pygame

from core.game import Game
from core.menu import Menu
from core.settings import Settings



def initialize():
    global SETTINGS, screen, procedure, clock, procedure, menu
    with open('settings.json', 'r') as data:
        SETTINGS = json.load(data)
    pygame.init()
    screen = pygame.display.set_mode((SETTINGS['WIDTH'], SETTINGS['HEIGHT']))
    play_soundtrack()
    clock = pygame.time.Clock()
    menu = Menu(screen)
    procedure = menu

def play_soundtrack():
    soundtrack = pygame.mixer.Sound(os.path.join('audio', 'Noisia_dustup.mp3'))
    soundtrack.play(loops=-1)
    soundtrack.set_volume(SETTINGS['SOUNDTRACK_VOLUME'])

if __name__ == '__main__':
    # Initialiazing pygame module and settings
    initialize()

    while True:
        procedure.run()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if str(procedure) == 'game':
                if event.type == game.ENEMY_GUNFIRE_EVENT:
                    game.enemies.gunfire()
                
                if not game.player.sprite.alive:
                    menu = Menu(screen, score=game.score)
                    procedure = menu

            elif str(procedure) == 'menu':
                if menu.button_exit.click():
                    pygame.quit()
                    sys.exit()

                if menu.button_run.click():
                    initialize()
                    game = Game(screen)
                    procedure = game

                if menu.button_settings.click():
                    pygame.quit()
                    settings = Settings()
                    if settings.run():
                        initialize()

        pygame.display.flip()
        clock.tick(SETTINGS['FPS'])