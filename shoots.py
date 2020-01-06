import pygame
from constant import *


class Bullet(pygame.sprite.Sprite):
    def __init__(self, cords, speed, *groups):
        pygame.sprite.Sprite.__init__(self, *groups)
        self.image = pygame.Surface((10, 10))
        self.image.fill((255, 0, 0))
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = cords
        self.speedy = speed

    def update(self):
        self.rect.y += self.speedy
        if self.rect.y - self.rect.h <= 0 or self.rect.y >= HEIGHT:
            self.kill()