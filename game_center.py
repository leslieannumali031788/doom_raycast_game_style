import pygame as pg
import sys
from settings import *
from map import *
from player import *
from raycasting import *
from object_renderer import *
from object_handler import *
from weapon import *
from sound import *
from path_finding import *

class Game:
    def __init__(self):
        pg.init()
        pg.mouse.set_visible(False)
        self.screen = pg.display.set_mode(RES)
        self.clock = pg.time.Clock()
        self.delta_time = 1
        self.global_trigger = False
        self.global_event = pg.USEREVENT + 0
        pg.time.set_timer(self.global_event, 40)
        self.game_over = False
        self.win = False
        self.new_game()

    def new_game(self):
        self.map = Map(self)
        self.player = Player(self)
        self.object_renderer = ObjectRenderer(self)
        self.raycasting = RayCasting(self)
        self.object_handler = ObjectHandler(self)
        self.pathfinding = PathFinding(self)
        self.sound = Sound(self)
        self.weapon = Weapon(self)
        self.game_over = False
        self.win = False

    def update(self):
        if not self.game_over and not self.win:
            self.player.update()
            self.raycasting.update()
            self.object_handler.update()
            self.weapon.update()

            if not any(npc.alive for npc in self.object_handler.npc_list):
                self.win = True
                print("VICTORY! Ubos ang kalaban.")

            if self.player.health <= 0:
                self.game_over = True

        self.delta_time = self.clock.tick(FPS)
        pg.display.set_caption(f'FPS: {self.clock.get_fps() :.1f}')

    def draw(self):
        self.object_renderer.draw()
        self.weapon.draw()

        if self.game_over:
            self.draw_end_message("GAME OVER", "red")
        elif self.win:
            self.draw_end_message("VICTORY!", "green")

        pg.display.flip()

    def draw_end_message(self, text, color):
        font = pg.font.SysFont('Arial', 100, bold=True)
        render = font.render(text, True, color)
        self.screen.blit(render, (HALF_WIDTH - render.get_width() // 2, HALF_HEIGHT - render.get_height() // 2))
        sub_font = pg.font.SysFont('Arial', 30)
        sub_render = sub_font.render("Press 'R' to Restart or 'ESC' to Quit", True, 'white')
        self.screen.blit(sub_render, (HALF_WIDTH - sub_render.get_width() // 2, HALF_HEIGHT + 100))

    def check_events(self):
        self.global_trigger = False
        for event in pg.event.get():
            if event.type == pg.QUIT or (event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE):
                pg.quit()
                sys.exit()
            
            if (self.game_over or self.win) and event.type == pg.KEYDOWN and event.key == pg.K_r:
                self.new_game()

            elif event.type == self.global_event:
                self.global_trigger = True

            if not self.game_over and not self.win:
                self.player.single_fire_event(event)

    def run(self):
        while True:
            self.check_events()
            self.update()
            self.draw()

if __name__ == '__main__':
    game = Game()
    game.run()