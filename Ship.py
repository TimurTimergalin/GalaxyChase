import pygame
from constant import *


class Ship(pygame.sprite.Sprite):
    def __init__(self, group, *groups):
        super(Ship, self).__init__(group)
        self.add(*groups)
        self.collide = False
        self.c = 1

    def update(self, *args):
        if self.collide:
            try:
                self.image = pygame.image.load(f'data/boom{self.c}')
                self.c += 1
            except Exception:
                self.kill()

    def shoot(self):
        pass


class Player(Ship):
    image = pygame.image.load('data/player.png')
    image.set_colorkey(image.get_at((0, 0)))

    def __init__(self, group, *groups):
        Ship.__init__(self, group, groups)
        self.speed = 360 / FPS
        self.image = Player.image
        self.rect = self.image.get_rect()
        self.rect.x = WIDTH // 2 + self.rect.width // 2
        self.rect.y = 500

    def update(self, *args):
        if args and args[0] == MOVE_RIGHT and self.rect.x + self.rect.width + self.speed <= WIDTH:
            self.rect = self.rect.move(self.speed, 0)
        if args and args[0] == MOVE_LEFT and self.rect.x - self.speed >= 0:
            self.rect = self.rect.move(-self.speed, 0)
        if args and args[0] == SHOOT_MADE:
            self.shoot()
        Ship.update(self, *args)