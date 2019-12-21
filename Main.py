import pygame
from constant import *
from Ship import *
pygame.init()

size = WIDTH, HEIGHT
screen = pygame.display.set_mode(size)

all_sprites = pygame.sprite.Group()
player = pygame.sprite.Group()
enemies = pygame.sprite.Group()

Player(all_sprites, player)
BackEnemy(all_sprites, enemies)
BackEnemy(all_sprites, enemies)

bg = pygame.image.load('data/background.png')
bg_y = 0

run = True
clock = pygame.time.Clock()
while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    keys = pygame.key.get_pressed()
    if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
        player.update(MOVE_RIGHT)
    if keys[pygame.K_LEFT] or keys[pygame.K_a]:
        player.update(MOVE_LEFT)
    if keys[pygame.BUTTON_LEFT] or keys[pygame.K_SPACE]:
        player.update(SHOOT_MADE)

    screen.blit(bg, (0, bg_y))
    screen.blit(bg, (0, bg_y - HEIGHT))
    bg_y += 1200 / FPS
    if bg_y >= HEIGHT:
        bg_y = 0
    all_sprites.update()
    all_sprites.draw(screen)
    pygame.display.flip()
    clock.tick(FPS)