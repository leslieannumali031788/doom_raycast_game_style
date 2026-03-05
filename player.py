from settings import *
import pygame as pg
import math

class Player:
    def __init__(self, game):
        self.game = game
        self.x, self.y = PLAYER_POS
        self.angle = PLAYER_ANGLE
        self.shot = False
        self.health = PLAYER_MAX_HEALTH
        self.rel = 0

    @property
    def pos(self): return self.x, self.y

    @property
    def map_pos(self): return int(self.x), int(self.y)

    def get_damage(self, damage):
        if self.health > 0:
            self.health -= damage
            print(f"Health: {self.health}")
            if self.game.sound and hasattr(self.game.sound, 'player_pain') and self.game.sound.player_pain:
                self.game.sound.player_pain.play()
            if self.health <= 0:
                self.health = 0
                print("GAME OVER!")

    def single_fire_event(self, event):
        if event.type == pg.MOUSEBUTTONDOWN:
            if event.button == 1 and not self.shot and self.game.weapon and not self.game.weapon.reloading:
                if self.game.sound and hasattr(self.game.sound, 'shotgun') and self.game.sound.shotgun:
                    self.game.sound.shotgun.play()
                self.shot = True
                self.game.weapon.reloading = True

    def movement(self):
        sin_a = math.sin(self.angle); cos_a = math.cos(self.angle)
        dx, dy = 0, 0
        speed = PLAYER_SPEED * self.game.delta_time
        keys = pg.key.get_pressed()
        if keys[pg.K_w]: dx += speed * cos_a; dy += speed * sin_a
        if keys[pg.K_s]: dx -= speed * cos_a; dy -= speed * sin_a
        if keys[pg.K_a]: dx += speed * sin_a; dy -= speed * cos_a
        if keys[pg.K_d]: dx -= speed * sin_a; dy += speed * cos_a
        self.check_wall_collision(dx, dy)
        self.angle %= math.tau

    def check_wall(self, x, y): return (x, y) not in self.game.map.world_map

    def check_wall_collision(self, dx, dy):
        scale = PLAYER_SIZE_SCALE / self.game.delta_time
        if self.check_wall(int(self.x + dx * scale), int(self.y)): self.x += dx
        if self.check_wall(int(self.x), int(self.y + dy * scale)): self.y += dy

    def mouse_control(self):
        mx, my = pg.mouse.get_pos()
        if mx < MOUSE_BORDER_LEFT or mx > MOUSE_BORDER_RIGHT: pg.mouse.set_pos([HALF_WIDTH, HALF_HEIGHT])
        self.rel = pg.mouse.get_rel()[0]
        self.rel = max(-MOUSE_MAX_REL, min(MOUSE_MAX_REL, self.rel))
        self.angle += self.rel * MOUSE_SENSITIVITY * self.game.delta_time

    def update(self):
        self.movement()
        self.mouse_control()
        if self.game.weapon and not self.game.weapon.reloading: self.shot = False