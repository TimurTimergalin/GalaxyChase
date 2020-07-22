import pygame
from constant import *
from Score import Score
pygame.init()


class Bullet(pygame.sprite.Sprite):  # Шаблон пули
    def __init__(self, cords, speed, target, *groups):
        pygame.sprite.Sprite.__init__(self, *groups)
        pygame.mixer.Sound('data/pew.wav').play()
        self.image = pygame.Surface((10, 10))
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = cords
        self.speedy = speed
        self.target = target

    def update(self):
        self.rect.y += self.speedy
        if self.rect.y - self.rect.h <= 0 or self.rect.y >= HEIGHT:
            self.kill()


class PlayerBullet(Bullet):  # Пуля игрока
    def __init__(self, cords, speed, target, *groups):
        super(PlayerBullet, self).__init__(cords, speed, target, *groups)
        self.image.fill((0, 0, 255))
        self.mask = pygame.mask.from_surface(self.image)

    def update(self):
        super(PlayerBullet, self).update()
        for i in self.target:
            if pygame.sprite.collide_rect(self, i):
                if i.collided:
                    continue
                self.kill()
                if not i.bulletproof:
                    i.collided = True
                    i.rect.x -= 64
                    i.rect.y -= 64
                    Score.add_score(100)
                break


class EnemyBullet(Bullet):  # Пуля врага
    def __init__(self, cords, speed, target, *groups):
        super(EnemyBullet, self).__init__(cords, speed, target, *groups)
        self.image.fill((255, 0, 0))
        self.mask = pygame.mask.from_surface(self.image)

    def update(self):
        super(EnemyBullet, self).update()
        for i in self.target:
            if i.collided:
                continue
            if pygame.sprite.collide_rect(self, i):
                self.kill()
                if 'shield' not in i.effects:
                    i.collided = True
                    i.rect.x -= 64
                    i.rect.y -= 64
                    pygame.mixer.music.stop()
                    Score.dead = True
                    pygame.time.set_timer(IS_DEAD, 1000)
                else:
                    pygame.mixer.Sound('data/damage.ogg').play()
                    i.effects.discard('shield')

