import pygame as pg
from settings import *

class ObjectRenderer:
    def __init__(self, game):
        self.game = game
        self.screen = game.screen
        self.wall_textures = self.load_wall_textures()
        try:
            self.sky_image = self.get_texture('resources/textures/sky.png', (WIDTH, HALF_HEIGHT))
        except:
            self.sky_image = pg.Surface((WIDTH, HALF_HEIGHT))
            self.sky_image.fill('blue')
        self.sky_offset = 0
        self.digits_font = pg.font.SysFont('Arial', 80, bold=True)

    def draw(self):
        self.draw_background()
        self.render_game_objects()
        self.draw_player_health()  # Dito nag-error kanina, dapat nandoon yung definition sa baba
        self.draw_crosshair()

    def draw_player_health(self):
        hp_display = str(max(0, int(self.game.player.health)))
        color = 'red' if self.game.player.health < 30 else 'white'
        health_render = self.digits_font.render(hp_display, False, color)
        self.screen.blit(health_render, (20, HEIGHT - 100))

    def draw_crosshair(self):
        pg.draw.circle(self.screen, 'red', (HALF_WIDTH, HALF_HEIGHT), 5, 2)

    def draw_background(self):
        self.sky_offset = (self.sky_offset + 4.0 * self.game.player.rel) % WIDTH
        self.screen.blit(self.sky_image, (-self.sky_offset, 0))
        self.screen.blit(self.sky_image, (-self.sky_offset + WIDTH, 0))
        pg.draw.rect(self.screen, FLOOR_COLOR, (0, HALF_HEIGHT, WIDTH, HEIGHT))

    def render_game_objects(self):
        list_objects = sorted(self.game.raycasting.objects_to_render, key=lambda t: t[0], reverse=True)
        for depth, image, pos in list_objects:
            self.screen.blit(image, pos)

    @staticmethod
    def get_texture(path, res=(TEXTURE_SIZE, TEXTURE_SIZE)):
        try:
            img = pg.image.load(path).convert_alpha()
            return pg.transform.scale(img, res)
        except:
            surf = pg.Surface(res)
            surf.fill((255, 0, 255))
            return surf

    def load_wall_textures(self):
        return {
            1: self.get_texture('resources/textures/1.png'),
            2: self.get_texture('resources/textures/2.png'),
            3: self.get_texture('resources/textures/3.png'),
            4: self.get_texture('resources/textures/4.png'),
            5: self.get_texture('resources/textures/5.png'),
        }