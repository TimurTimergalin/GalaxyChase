import pygame
from constant import *
import random


class Ship(pygame.sprite.Sprite):
    def __init__(self, *groups):
        super(Ship, self).__init__(groups)
        self.collide = False
        self.c = 1

    def update(self, *args):
        if self.collide:
            self.collided()

    def shoot(self):
        pass

    def collided(self):
        pass  # feature


class Player(Ship):
    image = pygame.image.load('data/player.png')
    image.set_colorkey(image.get_at((0, 0)))

    def __init__(self, *groups):
        Ship.__init__(self, groups)
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


class BackEnemy(Ship):
    image = pygame.image.load('data/back_enemy.png')
    image.set_colorkey(image.get_at((0, 0)))
    coord_x = 0

    def __init__(self, *groups):
        super(BackEnemy, self).__init__(groups)
        self.image = BackEnemy.image
        self.rect = self.image.get_rect()
        self.rect.x = BackEnemy.coord_x
        BackEnemy.coord_x = 250
        self.rect.y = HEIGHT - 50
        self.speed = 480

    def update(self, *args):
        if self.rect.x <= 0:
            self.speed *= -1
            self.rect.x += 10
        elif self.rect.x + self.rect.width >= WIDTH:
            self.speed *= -1
            self.rect.x -= 10
        else:
            self.rect.x += self.speed / FPS
        if random.randint(1, 50) == 1:
            self.speed *= -1


class FrontEnemy(Ship):
    image = pygame.image.load('data/front_enemy.png')
    image.set_colorkey(image.get_at((0, 0)))

    def __init__(self, *groups):
        super(FrontEnemy, self).__init__(groups)
        self.image = FrontEnemy.image
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, WIDTH - self.rect.width)
        self.rect.y = -self.rect.height - 1
        self.speed = 480

    def update(self, *args):
        self.rect = self.rect.move(0, self.speed / FPS)
        if self.rect.y >= HEIGHT:
            self.kill()