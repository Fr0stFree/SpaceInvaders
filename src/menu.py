import os

import pygame

from src.settings import Settings


class Button(pygame.sprite.Sprite):
    WIDTH, HEIGHT = 150, 40
    UNPRESSED_COLOR = '#475F77'
    HOVER_COLOR = '#D74B4B'
    ELEVATION = 5
    FONT_COLOR = '#EEEEEE'
    FONT_SIZE = 36

    def __init__(self, text, position, screen):
        super().__init__()
        self.screen = screen

        self.pressed = False
        self.elevation = self.ELEVATION
        self.button_level = position[1]

        self.button_color = self.UNPRESSED_COLOR
        self.button_rect = pygame.Rect(
            (position[0]-self.WIDTH//2, position[1]),
            (self.WIDTH, self.HEIGHT)
        )
        self.button_pressed_rect = pygame.Rect(
            (position[0]-self.WIDTH//2, position[1]),
            (self.WIDTH, self.ELEVATION)
        )
        self.button_pressed_color = '#354B5E'

        self.text = text
        self.text_font = pygame.font.Font(os.path.join('graphics', 'Pixeltype.ttf'), self.FONT_SIZE)
        self.text_surf = self.text_font.render(self.text, True, self.FONT_COLOR)
        self.text_rect = self.text_surf.get_rect(center=self.button_rect.center)

    def draw(self):
        self.button_rect.y = self.button_level - self.elevation
        self.text_rect.center = self.button_rect.center

        self.button_pressed_rect.midtop = self.button_rect.midtop
        self.button_pressed_rect.height = self.button_rect.height + self.elevation

        pygame.draw.rect(self.screen, self.button_pressed_color, self.button_pressed_rect, border_radius=12)
        pygame.draw.rect(self.screen, self.button_color, self.button_rect, border_radius=12)
        self.screen.blit(self.text_surf, self.text_rect)

    def click(self):
        mouse_position = pygame.mouse.get_pos()
        if not self.button_rect.collidepoint(mouse_position):
            self.elevation = self.ELEVATION
            self.button_color = self.UNPRESSED_COLOR
        else:
            self.button_color = self.HOVER_COLOR
            if pygame.mouse.get_pressed()[0]:
                self.elevation = 0
                self.pressed = True
            else:
                self.elevation = self.ELEVATION
                if self.pressed:
                    return True


class Menu:
    FONT_COLOR = (150, 150, 150)
    FONT_SIZE = 36
    BACKGROUND_IMAGE = pygame.image.load(os.path.join('graphics', 'background.jpg'))

    def __init__(self, screen, message):
        self.message = message
        self.background_surf = self.BACKGROUND_IMAGE.convert_alpha()
        self.background_rect = self.background_surf.get_rect(topleft=(0, 0))
        self.screen = screen
        self.button_run = Button(text='RUN', position=(0.5*Settings.WIDTH, 0.35*Settings.HEIGHT), screen=screen)
        self.button_exit = Button(text='EXIT', position=(0.5*Settings.WIDTH, 0.65*Settings.HEIGHT), screen=screen)
        self.button_settings = Button(text='SETTINGS', position=(0.5*Settings.WIDTH, 0.5*Settings.HEIGHT), screen=screen)
    
    def __str__(self):
        return 'menu'
    
    def run(self):
        self.screen.blit(self.background_surf, self.background_rect)
        self.button_run.draw()
        self.button_settings.draw()
        self.button_exit.draw()
        self.text_font = pygame.font.Font(os.path.join('graphics', 'Pixeltype.ttf'), self.FONT_SIZE)
        message_surf = self.text_font.render(self.message, False, self.FONT_COLOR)
        message_rect = message_surf.get_rect(center=(0.5*Settings.WIDTH, 0.15*Settings.HEIGHT))
        self.screen.blit(message_surf, message_rect)
