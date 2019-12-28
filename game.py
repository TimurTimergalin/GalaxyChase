import pygame
from constant import *
from Ship import *
from new_front_enemy import new_front_enemy
import sys


def game(screen):
    all_sprites = pygame.sprite.Group()
    player = pygame.sprite.Group()
    enemies = pygame.sprite.Group()

    Player(enemies, all_sprites, player)
    BackEnemy(player, all_sprites, enemies)
    BackEnemy(player, all_sprites, enemies)

    bg = pygame.image.load('data/background.png')
    bg_y = 0

    pygame.mixer.music.load('C:/Users/1/Documents/Python 3.6/GalaxyChase/data/gameplay.mp3')
    pygame.mixer.music.play(-1)

    run = True
    clock = pygame.time.Clock()
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.mixer.music.stop()
                    return start_screen(screen)

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

        new_front_enemy(player, all_sprites, enemies)
        all_sprites.update()
        all_sprites.draw(screen)
        pygame.display.flip()
        if not len(player):
            return start_screen(screen)
        clock.tick(FPS)


def start_screen(screen):
    pygame.mixer.music.load('C:/Users/1/Documents/Python 3.6/GalaxyChase/data/start.mp3')
    pygame.mixer.music.play()

    clock = pygame.time.Clock()
    run = True
    bg = pygame.image.load('data/background.png')
    planet = pygame.image.load('data/planet1.png')
    planet_x = WIDTH // 2 - planet.get_width() // 2
    planet.set_colorkey(planet.get_at((0, 0)))
    bg_y = 0
    dy = 0
    dy1 = 0
    pygame.time.set_timer(GOING_DOWN, 1000)
    go_down = False
    font = pygame.font.SysFont('arialblack', 30)

    while run:
        screen.blit(bg, (0, bg_y))
        screen.blit(bg, (0, bg_y - HEIGHT))
        text = font.render('Galaxy Chase', 1, (255, 200, 0))
        screen.blit(text, ((WIDTH - text.get_width()) // 2, (HEIGHT - text.get_height()) // 2 + dy))
        screen.blit(planet, (planet_x, -HEIGHT // 2 - planet.get_height() + dy1))
        if go_down:
            dy += 50 / FPS
            dy1 += 50 / FPS
            bg_y += 50 / FPS
            if dy >= HEIGHT + text.get_height():
                go_down = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit(0)
            if event.type == GOING_DOWN:
                go_down = True
                pygame.time.set_timer(GOING_DOWN, 0)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit(0)
                else:
                    if go_down:
                        bg_y = text.get_height()
                        dy1 = HEIGHT + text.get_height()
                        dy = HEIGHT + text.get_height()
                        go_down = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if go_down:
                    bg_y = text.get_height()
                    dy1 = HEIGHT + text.get_height()
                    dy = HEIGHT + text.get_height()
                    go_down = False
                elif planet_x <= event.pos[0] <= planet_x + planet.get_width() and \
                        -HEIGHT // 2 - planet.get_height() + dy1 <= event.pos[1] <=\
                        -HEIGHT // 2 - planet.get_height() + dy1 + planet.get_height():
                    pygame.mixer.music.stop()
                    return game(screen)
        pygame.display.flip()
        clock.tick(FPS)