import pygame
from constant import *
pygame.init()


class Bonus(pygame.sprite.Sprite):
    def __init__(self, player, *groups):
        super(Bonus, self).__init__(*groups)
        self.speed = 1200 / FPS
        self.player = player

    def effect(self, player):
        return

    def update(self):
        for i in self.player:
            if pygame.sprite.collide_mask(self, i):
                self.effect(i)
                self.kill()