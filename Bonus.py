import pygame
import random
from constant import *
from Ship import *
pygame.init()


class Bonus(pygame.sprite.Sprite):
    def __init__(self, player, enemy=None, *groups):
        super(Bonus, self).__init__(*groups)
        self.player = player

    def effect(self, player):
        return

    def update(self):
        for i in self.player:
            if pygame.sprite.collide_mask(self, i):
                self.effect(i)
                self.kill()


class Shield(Bonus):
    image = pygame.image.load('data/shield.png')
    image.set_colorkey(image.get_at((0, 0)))
    chance = 10000

    def __init__(self, player, enemy=None, *groups):
        super(Shield, self).__init__(player, enemy, *groups)
        self.image = Shield.image
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, WIDTH - self.rect.width)
        self.rect.y = -self.rect.height - 1
        self.mask = pygame.mask.from_surface(self.image)
        self.speed = 240 / FPS

    def effect(self, player):
        player.effects.add('shield')

    def update(self):
        self.rect = self.rect.move(0, self.speed)
        if self.rect.y >= HEIGHT:
            self.kill()
        super().update()


class Bomb(Bonus):
    image = pygame.image.load('data/bomb.png')
    image.set_colorkey(image.get_at((1, 0)))
    chance = 12000

    def __init__(self, player, enemy, *groups):
        super().__init__(player, enemy, *groups)
        self.enemy = enemy
        self.image = Bomb.image
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, WIDTH - self.rect.width)
        self.rect.y = -self.rect.height - 1
        self.mask = pygame.mask.from_surface(self.image)
        self.speed = 240 / FPS

    def effect(self, player=None):
        for i in self.enemy:
            if type(i) == BackEnemy:
                continue
            i.collided = True


    def update(self):
        self.rect = self.rect.move(0, self.speed)
        if self.rect.y >= HEIGHT:
            self.kill()
        super().update()