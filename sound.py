import pygame as pg

class Sound:
    def __init__(self, game):
        self.game = game
        pg.mixer.init()
        self.path = 'resources/sound/'
        self.shotgun = self.load_sound('shotgun.wav')
        self.npc_pain = self.load_sound('npc_pain.wav')
        self.npc_death = self.load_sound('npc_death.wav')
        self.npc_shot = self.load_sound('npc_attack.wav') # Siguraduhin na may 'npc_attack.wav' sa folder
        self.player_pain = self.load_sound('player_pain.wav')

    def load_sound(self, filename):
        try:
            return pg.mixer.Sound(self.path + filename)
        except:
            print(f"ALERTO: Kulang ang file: {filename}")
            return None