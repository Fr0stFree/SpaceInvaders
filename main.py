import sys
import os
import pygame

import settings
from player import Player
from weapons import Explosion
from enemies import ExtraEnemy, EnemyGroup


class Button:
    WIDTH, HEIGHT = 150, 40
    UNPRESSED_COLOR = '#475F77'
    HOVER_COLOR = '#D74B4B'
    ELEVATION = 5
    FONT_COLOR = '#EEEEEE'
    FONT_SIZE = 36

    def __init__(self, text, position):
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

        pygame.draw.rect(screen, self.button_pressed_color, self.button_pressed_rect, border_radius=12)
        pygame.draw.rect(screen, self.button_color, self.button_rect, border_radius=12)
        screen.blit(self.text_surf, self.text_rect)
        self.click()

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

    def __init__(self, score=0):
        self.background_surf = self.BACKGROUND_IMAGE.convert_alpha()
        self.background_rect = self.background_surf.get_rect(topleft=(0, 0))
        self.score = score
        self.button_run = Button(text='RUN', position=(0.5*settings.WIDTH, 0.35*settings.HEIGHT))
        self.button_settings = Button(text='SETTINGS', position=(0.5*settings.WIDTH, 0.5*settings.HEIGHT))
        self.button_exit = Button(text='EXIT', position=(0.5*settings.WIDTH, 0.65*settings.HEIGHT))
    
    def __str__(self):
        return 'menu'
    
    def run(self):
        screen.blit(self.background_surf, self.background_rect)
        self.button_run.draw()
        self.button_settings.draw()
        self.button_exit.draw()
        if self.score:
            self.text_font = pygame.font.Font(os.path.join('graphics', 'Pixeltype.ttf'), self.FONT_SIZE)
            score_surf = self.text_font.render(f'your score: {self.score}', False, self.FONT_COLOR)
            score_rect = score_surf.get_rect(center=(0.5*settings.WIDTH, 0.15*settings.HEIGHT))
            screen.blit(score_surf, score_rect)


class Game:
    BACKGROUND_IMAGE = pygame.image.load(os.path.join('graphics', 'background.jpg'))
    HEALTH_IMAGE = pygame.image.load(os.path.join('graphics', 'player_ship.png'))
    HEALTH_SIZE = (31, 29)
    FONT_SIZE = 26
    FONT_COLOR = (255, 255, 255)
    ENEMIES_BEFORE_THE_BOSS = 12
    EXTRA_ENEMY_APPEARANCE_TIME = 1000

    def __init__(self):
        self.background_surf = self.BACKGROUND_IMAGE.convert_alpha()
        self.background_rect = self.background_surf.get_rect(topleft=(0, 0))

        self.player = pygame.sprite.GroupSingle(Player())
        self.live_surf = pygame.transform.scale(self.HEALTH_IMAGE.convert_alpha(), self.HEALTH_SIZE)

        self.extra_enemy = pygame.sprite.GroupSingle()
        self.extra_enemy_spawn = self.EXTRA_ENEMY_APPEARANCE_TIME

        self.enemies = EnemyGroup()
        self.enemies.setup()

        self.explosions = pygame.sprite.Group()

        self.score = 0
        self.font = pygame.font.Font(os.path.join('graphics', 'Pixeltype.ttf'), self.FONT_SIZE)

    def __str__(self):
        return 'game'

    def display_background(self):
        screen.blit(self.background_surf, self.background_rect)

    def display_lives(self):
        for live in range(self.player.sprite.health-1):
            position = (settings.WIDTH - (self.HEALTH_SIZE[1] * 2 + 25) + (live * (self.HEALTH_SIZE[1]+10)), 10)
            screen.blit(self.live_surf, position)
    
    def display_score(self):
        score_surf = self.font.render(f'score: {self.score}', False, self.FONT_COLOR)
        score_rect = score_surf.get_rect(topleft=(0.05*settings.WIDTH, 0.95*settings.HEIGHT))
        screen.blit(score_surf, score_rect)

    def extra_enemy_appearance(self):
        if len(self.enemies.sprites) < self.ENEMIES_BEFORE_THE_BOSS:
            if not self.extra_enemy:
                self.extra_enemy_spawn -= 1
            if self.extra_enemy_spawn <= 0:
                self.extra_enemy.add(ExtraEnemy())
                self.extra_enemy_spawn = self.EXTRA_ENEMY_APPEARANCE_TIME

    def projectile_collisions_system(self):
        #  Коллизии ракет игрока
        missiles = self.player.sprite.missiles
        if missiles:
            for missile in missiles:
                if pygame.sprite.spritecollide(missile, self.enemies.sprites, True):
                    explosion = Explosion(missile.rect.center)
                    self.explosions.add(explosion)
                    missile.sound_effect.stop()
                    missile.kill()
                    self.score += 1
                if pygame.sprite.spritecollide(missile, self.extra_enemy, True):
                    explosion = Explosion(missile.rect.center)
                    self.explosions.add(explosion)
                    missile.sound_effect.stop()
                    missile.kill()
                    self.score += 5

        # Коллизии лазеров противника
        lasers = self.enemies.lasers
        if lasers:
            for laser in lasers:
                if pygame.sprite.spritecollide(laser, self.player, False):
                    laser.kill()
                    self.player.sprite.health -= 1

        # Коллизии луча специального противника
        if self.extra_enemy:
            beam = self.extra_enemy.sprite.beam.sprite
            if beam:
                if pygame.sprite.spritecollide(beam, self.player, False):
                    self.player.sprite.health -= 1

    def run(self):
        #  Обновление фона и вспомогательной информации
        self.display_background()
        self.display_score()
        self.display_lives()

        #  Обновление игрока
        if self.player.sprite.health > 0:
            self.player.update()
        else:
            self.player.sprite.explode()

        self.player.draw(screen)
        self.player.sprite.missiles.draw(screen)

        #  Обновление специального противника
        self.extra_enemy_appearance()
        if self.extra_enemy:
            self.extra_enemy.update()
            self.extra_enemy.sprite.beam.draw(screen)
            self.extra_enemy.draw(screen)

        #  Обновление группы противников
        if self.enemies.sprites:
            self.enemies.sprites.update()
            self.enemies.sprites.draw(screen)
            self.enemies.movement()
            self.enemies.lasers.update()
            self.enemies.lasers.draw(screen)
        else:
            self.score += 5
            self.enemies.setup()

        #  Отображение взрывов
        if self.explosions:
            self.explosions.draw(screen)
            self.explosions.update()

        # Проверка коллизий
        self.projectile_collisions_system()

def play_music():
    soundtrack = pygame.mixer.Sound(os.path.join('audio', 'Noisia_dustup.mp3'))
    soundtrack.play(loops=-1)
    soundtrack.set_volume(0.25)

if __name__ == '__main__':
    pygame.init()
    screen = pygame.display.set_mode((settings.WIDTH, settings.HEIGHT))
    play_music()
    clock = pygame.time.Clock()
    menu = Menu()
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
                    menu = Menu(game.score)
                    procedure = menu
                
            elif str(procedure) == 'menu':
                if menu.button_exit.click():
                    pygame.quit()
                    sys.exit()

                if menu.button_run.click():
                    game = Game()
                    procedure = game

        pygame.display.flip()
        clock.tick(settings.FPS)