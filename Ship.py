import pygame
from constant import *
import random
from shoots import *
from Score import Score

pygame.init()


class Ship(pygame.sprite.Sprite):  # Шаблон корабля
    boom = pygame.image.load('data/boom.png')

    def __init__(self, bullets, *groups):
        super(Ship, self).__init__(groups)
        self.collided = False
        self.frames = []
        self.cut_sheet(Ship.boom, BOOM_WIDTH, BOOM_HEIGHT)
        self.cur_frame = 0
        self.bullets = bullets
        self.bulletproof = False

    def update(self, *args):
        if self.collided:
            self.collide()

    def shoot(self, type_, cords, speed, target, *groups):  # Метод выстрела
        if type_ == 'player':
            PlayerBullet(cords, speed, target, *groups)
        else:
            EnemyBullet(cords, speed, target, *groups)

    def collide(self):  # Метод взрыва
        pygame.mixer.Sound('data/death.ogg').play()
        try:
            self.image = self.frames[self.cur_frame]
            self.cur_frame += 1
        except IndexError:
            self.kill()

    def cut_sheet(self, sheet, columns, rows):  # Метод разрезания спрайтов
        self.new_rect = pygame.Rect(0, 0, sheet.get_width() // columns,
                                    sheet.get_height() // rows)
        for j in range(rows):
            for i in range(columns):
                frame_location = (self.new_rect.w * i, self.new_rect.h * j)
                self.frames.append(sheet.subsurface(pygame.Rect(
                    frame_location, self.new_rect.size)))


class Player(Ship):  # Корабль игрока
    image = pygame.image.load('data/player.png')
    image.set_colorkey(image.get_at((0, 0)))

    def __init__(self, bullets, enemy_group, *groups):
        Ship.__init__(self, bullets, *groups)
        self.enemy_group = enemy_group
        self.effects = set()
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
            self.shoot('player', (self.rect.x + self.rect.w // 2, self.rect.y), -2000 / FPS, self.enemy_group, self.bullets)
        if args and args[0] == MOVE_FORWARD:
            self.rect = self.rect.move(0, -480 / FPS)
            if self.rect.y < - self.rect.w:
                self.kill()
        for i in self.enemy_group:
            if pygame.sprite.collide_mask(self, i):
                if i.collided:
                    continue
                if 'shield' not in self.effects:
                    self.collided = True
                    self.rect.x -= 64
                    self.rect.y -= 64
                    i.kill()
                    pygame.mixer.music.stop()
                    Score.dead = True
                    pygame.time.set_timer(IS_DEAD, 1000)
                else:
                    pygame.mixer.Sound('data/damage.ogg').play()
                    self.effects.discard('shield')
                    i.collided = True
                    i.rect = i.rect.move(-64, -64)
                break
        Ship.update(self, *args)


class BackEnemy(Ship):  # Враг, летящий сзади игрока
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
            self.shoot('enemy', (self.rect.x + self.rect.w // 2, self.rect.y), -1500 / FPS, self.player, self.bullets)
        Ship.update(self, *args)


class FrontEnemy(Ship):  # Обычный враг
    image = pygame.image.load('data/front_enemy.png')
    image.set_colorkey(image.get_at((0, 0)))
    chance = 50

    def __init__(self, bullets, player, *groups):
        super(FrontEnemy, self).__init__(bullets, *groups)
        self.player = player
        self.image = FrontEnemy.image
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, WIDTH - self.rect.width)
        self.rect.y = -self.rect.height - 1
        self.speed = 480
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
                    Score.dead = True
                    pygame.time.set_timer(IS_DEAD, 1000)
                else:
                    pygame.mixer.Sound('data/damage.ogg').play()
                    i.effects.discard('shield')

        if random.randint(1, 150) == 1:
            self.shoot('enemy', (self.rect.x + self.rect.w // 2, self.rect.y), 1500 / FPS, self.player, self.bullets)

        Ship.update(self, *args)


class Kamikaze(Ship):  # Быстрый враг-камикадзе
    chance = 75
    image = pygame.image.load('data/kamikaze.png')
    image.set_colorkey(image.get_at((1, 0)))

    def __init__(self, bullets, player, *groups):
        super(Kamikaze, self).__init__(bullets, *groups)
        self.player = player
        self.image = Kamikaze.image
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, WIDTH - self.rect.width)
        self.rect.y = -self.rect.height - 1
        self.speed = 1440
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


class ShipTower(Ship):  # Турель корабля-базы Альянса
    image = pygame.image.load('data/ship_tower.png')
    image.set_colorkey(image.get_at((0, 0)))

    def __init__(self, bullets, enemy, *groups):
        super().__init__(bullets, groups)
        self.rect = self.image.get_rect()
        self.rect.x = 0
        self.rect.y = -90
        self.speed_x = 480
        self.speed_y = 1200
        self.enemy = enemy
        self.shot = True

    def update(self):
        self.rect = self.rect.move(self.speed_x / FPS, self.speed_y / FPS)
        if self.shot:
            self.shoot('player', (self.rect.x + self.rect.w // 2, self.rect.y), 3000 / FPS, self.enemy, self.bullets)

    def stop_x(self):
        self.speed_x = 0

    def stop_y(self):
        self.speed_y = 0

    def stop_shoot(self):
        self.shot = False


class Giant(Ship):  # Медленный, большой враг
    chance = 150
    image = pygame.image.load('data/giant.png')
    image.set_colorkey(image.get_at((0, 0)))

    def __init__(self, bullets, player, *groups):
        super(Giant, self).__init__(bullets, *groups)
        self.player = player
        self.image = Giant.image
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, WIDTH - self.rect.w)
        self.rect.y = -self.rect.h - 1
        self.speed = 400
        self.mask = pygame.mask.from_surface(self.image)
        self.bulletproof = True

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

        if random.randint(1, 50) == 1:
            self.shoot('enemy', (self.rect.x + self.rect.w // 2, self.rect.y), 1500 / FPS, self.player, self.bullets)

        Ship.update(self, *args)
