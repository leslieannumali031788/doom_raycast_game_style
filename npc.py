from sprite_object import *
import math

class NPC(AnimatedSprite):
    def __init__(self, game, path, pos=(10.5, 5.5), scale=0.6, shift=0.38, animation_time=180):
        super().__init__(game, path, pos, scale, shift, animation_time)
        base_path = path.rsplit('/', 1)[0]
        self.attack_images = self.get_images(base_path + '/attack')
        self.death_images = self.get_images(base_path + '/death')
        self.idle_images = self.get_images(base_path + '/idle')
        self.pain_images = self.get_images(base_path + '/pain')
        self.walk_images = self.get_images(base_path + '/walk')

        self.alive = True
        self.pain = False
        self.health = 100
        self.speed = 0.03
        self.attack_dist = 1.5
        self.frame_counter = 0

    def update(self):
        self.check_animation_time()
        self.get_sprite()
        self.run_logic()

    def check_hit_in_npc(self):
        if self.game.player.shot and self.norm_dist < 10:
            if HALF_WIDTH - self.sprite_half_width < self.screen_x < HALF_WIDTH + self.sprite_half_width:
                if self.game.sound and self.game.sound.npc_pain:
                    self.game.sound.npc_pain.play()
                self.game.player.shot = False
                self.pain = True
                self.health -= 50
                if self.health < 1:
                    self.alive = False
                    if self.game.sound and self.game.sound.npc_death:
                        self.game.sound.npc_death.play()

    def run_logic(self):
        if self.alive:
            self.check_hit_in_npc()
            if self.pain:
                self.animate(self.pain_images)
                if self.animation_trigger:
                    self.pain = False
            else:
                dist = math.hypot(self.game.player.x - self.x, self.game.player.y - self.y)
                if dist < 12:
                    if dist < self.attack_dist:
                        self.animate(self.attack_images)
                        self.attack()
                    else:
                        self.animate(self.walk_images)
                        self.movement()
                else:
                    self.animate(self.idle_images)
        else:
            self.animate_death()

    def attack(self):
        if self.animation_trigger and self.game.player.health > 0:
            if self.game.sound and hasattr(self.game.sound, 'npc_shot') and self.game.sound.npc_shot:
                self.game.sound.npc_shot.play()

            self.game.player.get_damage(0.5)

    def animate_death(self):
        if not self.alive and self.game.global_trigger:
            if self.frame_counter < len(self.death_images) - 1:
                self.frame_counter += 1
                self.image = self.death_images[self.frame_counter]

    def movement(self):
        next_pos = self.game.pathfinding.get_path(self.map_pos, self.game.player.map_pos)
        if next_pos != self.map_pos:
            next_x, next_y = next_pos
            angle = math.atan2(next_y + 0.5 - self.y, next_x + 0.5 - self.x)
            self.x += math.cos(angle) * self.speed
            self.y += math.sin(angle) * self.speed

    @property
    def map_pos(self):
        return int(self.x), int(self.y)
# --- NPC VARIANTS ---
class SoldierNPC(NPC):
    def __init__(self, game, pos=(10.5, 5.5)):
        super().__init__(game, 'resources/sprites/npc/soldier/0.png', pos)

class CacoDemonNPC(NPC):
    def __init__(self, game, pos=(10.5, 6.5)):
        super().__init__(game, 'resources/sprites/npc/caco_demon/0.png', pos, scale=0.7, shift=0.27)

class CyberDemonNPC(NPC):
    def __init__(self, game, pos=(11.5, 6.0)):
        super().__init__(game, 'resources/sprites/npc/cyber_demon/0.png', pos, scale=1.0, shift=0.04)