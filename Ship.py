import pygame
from constant import *
import random
from shoots import Bullet


class Ship(pygame.sprite.Sprite):
    boom = pygame.image.load('data/boom.png')

    def __init__(self, bullets, *groups):
        super(Ship, self).__init__(groups)
        self.collided = False
        self.frames = []
        self.cut_sheet(Ship.boom, BOOM_WIDTH, BOOM_HEIGHT)
        self.cur_frame = 0
        self.bullets = bullets

    def update(self, *args):
        if self.collided:
            self.collide()

    def shoot(self, cords, speed, *groups):
        Bullet(cords, speed, *groups)

    def collide(self):
        try:
            self.image = self.frames[self.cur_frame]
            self.cur_frame += 1
        except IndexError:
            self.kill()

    def cut_sheet(self, sheet, columns, rows):
        self.new_rect = pygame.Rect(0, 0, sheet.get_width() // columns,
                                    sheet.get_height() // rows)
        for j in range(rows):
            for i in range(columns):
                frame_location = (self.new_rect.w * i, self.new_rect.h * j)
                self.frames.append(sheet.subsurface(pygame.Rect(
                    frame_location, self.new_rect.size)))


class Player(Ship):
    image = pygame.image.load('data/player.png')
    image.set_colorkey(image.get_at((0, 0)))

    def __init__(self, bullets, enemy_group, *groups):
        Ship.__init__(self, bullets, *groups)
        self.enemy_group = enemy_group
        self.speed = 360 / FPS
        self.image = Player.image
        self.rect = self.image.get_rect()
        self.rect.x = WIDTH // 2 + self.rect.width // 2
        self.rect.y = 500
        self.mask = pygame.mask.from_surface(self.image)

    def update(self, *args):
        if args and args[0] == MOVE_RIGHT and self.rect.x + self.rect.width + self.speed <= WIDTH:
            self.rect = self.rect.move(self.speed, 0)
        if args and args[0] == MOVE_LEFT and self.rect.x - self.speed >= 0:
            self.rect = self.rect.move(-self.speed, 0)
        if args and args[0] == SHOOT_MADE:
            self.shoot((self.rect.x + self.rect.w // 2, self.rect.y), -2000 / FPS, self.bullets)
        for i in self.enemy_group:
            if pygame.sprite.collide_mask(self, i):
                self.collided = True
                self.rect.x -= 64
                self.rect.y -= 64
                i.kill()
                break
        Ship.update(self, *args)


class BackEnemy(Ship):
    image = pygame.image.load('data/back_enemy.png')
    image.set_colorkey(image.get_at((0, 0)))
    coord_x = 0

    def __init__(self, bullets, player, *groups):
        super(BackEnemy, self).__init__(bullets, *groups)
        self.player = player
        self.image = BackEnemy.image
        self.rect = self.image.get_rect()
        self.rect.x = BackEnemy.coord_x
        BackEnemy.coord_x = 250
        self.rect.y = HEIGHT - 50
        self.speed = 240
        self.mask = pygame.mask.from_surface(self.image)
        self.groups = groups

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
        if random.randint(1, 250) == 1:
            self.shoot((self.rect.x + self.rect.w // 2, self.rect.y), -2000 / FPS, self.bullets)
        Ship.update(self, *args)


class FrontEnemy(Ship):
    image = pygame.image.load('data/front_enemy.png')
    image.set_colorkey(image.get_at((0, 0)))

    def __init__(self, bullets, player, *groups):
        super(FrontEnemy, self).__init__(bullets, *groups)
        self.player = player
        self.image = FrontEnemy.image
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, WIDTH - self.rect.width)
        self.rect.y = -self.rect.height - 1
        self.speed = 360
        self.mask = pygame.mask.from_surface(self.image)

    def update(self, *args):
        self.rect = self.rect.move(0, self.speed / FPS)
        if self.rect.y >= HEIGHT:
            self.kill()

        for i in self.player:
            if pygame.sprite.collide_mask(self, i):
                self.collided = True
                self.rect.x -= 64
                self.rect.y -= 64
                i.kill()

        Ship.update(self, *args)


class Kamikaze(Ship):
    image = pygame.image.load('data/kamikaz.png')
    image.set_colorkey(image.get_at((0, 0)))

    def __init__(self, bullets, player, *groups):
        super(Kamikaze, self).__init__(bullets, *groups)
        self.player = player
        self.image = Kamikaze.image
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, WIDTH - self.rect.width)
        self.rect.y = -self.rect.height - 1
        self.speed = 720
        self.mask = pygame.mask.from_surface(self.image)

    def update(self, *args):
        self.rect = self.rect.move(0, self.speed / FPS)
        if self.rect.y >= HEIGHT:
            self.kill()

        for i in self.player:
            if pygame.sprite.collide_mask(self, i):
                self.collided = True
                self.rect.x -= 64
                self.rect.y -= 64
                i.kill()

        Ship.update(self, *args)


class Undine(Ship):
    chance = 40
    #image = pygame.image.load('data/kamikaze.png')
    #image.set_colorkey(image.get_at((1, 0)))

    def __init__(self, bullets, player, *groups):
        super(Undine, self).__init__(bullets, *groups)
        self.player = player
        self.image = Kamikaze.image
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, 100)
        self.rect.y = 700
        self.speed = 400
        self.mask = pygame.mask.from_surface(self.image)

    def update(self, *args):
        self.rect = self.rect.move(0, self.speed / FPS)
        if self.rect.y >= HEIGHT:
            self.kill()

        for i in self.player:
            if self.collided:
                break
            if pygame.sprite.collide_mask(self, i):
                self.collided = True
                self.rect = self.rect.move(-64, -64)
                if 'shield' not in i.effects:
                    i.kill()
                    pygame.mixer.music.stop()
                    pygame.time.set_timer(IS_DEAD, 1000)
                else:
                    i.effects.discard('shield')
                    pygame.mixer.Sound('data/damage.ogg').play()

        Ship.update(self, *args)
