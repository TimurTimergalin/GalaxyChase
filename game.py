import pygame
from constant import *
from Ship import *
from Bonus import *
from new_front_enemy import new_front_enemy
from new_bonus import new_bonus
import sys
from Score import Score


def game(screen):
    bullets = pygame.sprite.Group()
    all_sprites = pygame.sprite.Group()
    player = pygame.sprite.Group()
    enemies = pygame.sprite.Group()
    bonuses = pygame.sprite.Group()
    towers = pygame.sprite.Group()

    score = open('data/scores.scr')
    record = int(score.readline().strip())
    ending_got = score.readline().strip()
    if ending_got == 'False':
        ending_got = False
    else:
        ending_got = True
    score.close()

    ending = False

    Player(bullets, enemies, all_sprites, player)
    BackEnemy(bullets, player, all_sprites, enemies)
    BackEnemy(bullets, player, all_sprites, enemies)

    bg = pygame.image.load('data/background.png')
    bg_y = 0

    ship_y = 0
    ship_platform = pygame.image.load('data/platform.png')
    ship_top = pygame.image.load('data/top.png')

    pygame.mixer.music.load('data/gameplay.mp3')
    pygame.mixer.music.play(-1)

    run = True
    clock = pygame.time.Clock()
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:  # and not ending:
                    pygame.mixer.music.stop()
                    if Score.score > record:
                        new_score = open('data/scores.scr', 'w')
                        new_score.write(str(int(Score.score)) + '\n')
                        new_score.write('False')
                        new_score.close()
                    Score.clear()
                    return start_screen(screen, False)
                if event.key == pygame.K_SPACE:
                    player.update(SHOOT_MADE)
            if event.type == IS_DEAD:
                pygame.time.set_timer(IS_DEAD, 0)
                Score.clear()
                return start_screen(screen, False)
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == pygame.BUTTON_LEFT:
                    player.update(SHOOT_MADE)
                    Score.add_score(-5)
            if event.type == TOWER_ON:
                pygame.time.set_timer(TOWER_ON, 0)
                pygame.mixer.Sound('data/damage.ogg').play()
                for i in player:
                    i.effects.discard('tower')

        keys = pygame.key.get_pressed()
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            player.update(MOVE_RIGHT)
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            player.update(MOVE_LEFT)
        if keys[pygame.K_SPACE]:
            for i in player:
                if 'tower' in i.effects:
                    player.update(SHOOT_MADE)

        buttons = pygame.mouse.get_pressed()
        if buttons[0]:
            for i in player:
                if 'tower' in i.effects:
                    player.update(SHOOT_MADE)

        screen.blit(bg, (0, bg_y))
        screen.blit(bg, (0, bg_y - HEIGHT))
        if ship_y <= 100:
            bg_y += 1200 / FPS
        if bg_y >= HEIGHT:
            bg_y = 0

        if int(Score.score) >= 5000 and not ending_got:
            ending = True
            Score.dead = True

        if ending:
            screen.blit(ship_platform, (0, -100 + ship_y))

        score_font = pygame.font.SysFont('arialblack', 20)

        if not ending:
            new_front_enemy(player, bullets, all_sprites, enemies)
            new_bonus(player, enemies, all_sprites, bonuses)
        if ship_y >= 100:
            player.update(MOVE_FORWARD)
        all_sprites.update()
        all_sprites.draw(screen)
        bullets.update()
        bullets.draw(screen)
        if not ending:
            for i in player:
                for j in i.effects:
                    if j == 'shield':
                        screen.blit(pygame.transform.scale(Shield.image, (22, 23)), (325, 5))
                    elif j == 'tower':
                        screen.blit(pygame.transform.scale(Tower.image, (10, 25)), (300, 5))

        text = score_font.render(Score.get_score(), 1, (255, 255, 255))
        if not ending:
            screen.blit(text, (0, 0))
        Score.add_score(BASE_SCORE)
        if not len(player) and not ending:
            font = pygame.font.SysFont('arialblack', 50)
            if int(Score.score) > record:
                text = 'HIGH SCORE'
                new_score = open('data/scores.scr', 'w')
                new_score.write(str(int(Score.score)) + '\n')
                new_score.write(str(ending_got))
                new_score.close()
            else:
                text = 'GAME OVER'
            screen.blit(font.render(text, 1, (255, 0, 0)), (0, 325))

        elif not len(player) and ending:
            new_score = open('data/scores.scr', 'w')
            new_score.write(str(int(Score.score)) + '\n')
            new_score.write(str(True))
            new_score.close()
            pygame.mixer.music.stop()
            return titles(screen)

        if ending:
            screen.blit(ship_top, (0, ship_y - 100))
            if not len(towers):
                ShipTower(bullets, enemies, towers)
            if ship_y < 100:
                ship_y += 1200 / FPS
            else:
                ship_y = 100
                for i in towers:
                    i.stop_y()

            for i in towers:
                if i.rect.x == WIDTH - i.rect.w:
                    i.stop_x()
                    i.stop_shoot()
            towers.update()
            towers.draw(screen)
        pygame.display.flip()
        clock.tick(FPS)


def start_screen(screen, first_time=True, music=True):
    if music:
        pygame.mixer.music.load('data/start.mp3')
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
        text = font.render('Galaxy Chase', 1, (255, 200, 0))
        if not first_time:
            bg_y = 0
            dy1 = HEIGHT + text.get_height()
            dy = HEIGHT + text.get_height()
            go_down = False
        screen.blit(bg, (0, bg_y))
        screen.blit(bg, (0, bg_y - HEIGHT))
        if first_time:
            screen.blit(text, ((WIDTH - text.get_width()) // 2, (HEIGHT - text.get_height()) // 2 + dy))
        else:
            screen.blit(text, (65, 220))
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
                    Score.dead = False
                    if first_time:
                        return controls_screen(screen)
                    else:
                        pygame.mixer.music.stop()
                        return game(screen)
        pygame.display.flip()
        clock.tick(FPS)


def controls_screen(screen):
    clock = pygame.time.Clock()
    run = True
    font = pygame.font.SysFont('arialblack', 24)

    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    run = False
                else:
                    pygame.mixer.music.stop()
                    return game(screen)
            if event.type == pygame.MOUSEBUTTONDOWN:
                pygame.mixer.music.stop()
                return game(screen)

        screen.fill((0, 0, 0))

        text1 = 'move: W and S or \u2190 and \u2192'
        text2 = 'shoot: SPACE or MOUSE1'
        text3 = 'main menu: ESCAPE'

        sur1 = font.render(text1, 1, (255, 255, 255))
        sur2 = font.render(text2, 1, (255, 255, 255))
        sur3 = font.render(text3, 1, (255, 255, 255))

        screen.blit(sur1, (4, 200))
        screen.blit(sur2, (4, 400))
        screen.blit(sur3, (4, 300))

        pygame.display.flip()
        clock.tick(FPS)


def titles(screen):
    pygame.mixer.music.load('data/start.mp3')
    pygame.mixer.music.play()
    text = '''Our hero reached the Alliance  Base.
The   intelligence that he had  stolen
from   Empire  will  definitely     help
the     Confederation   to    save   the
galaxy     from    H.U.G.E.     Empire's
hegemony.     The    captain    of  the
"Fastest Lily" was    raised to  major
of the United Navy  of Confederation.
Glory      to    the    Alliance,   Major!'''.split('\n')

    thanks = 'Thank you for playing!'
    endings = '"Galaxy Chase" v1.0, TimurTimergalin and Denk, 2020'
    font1 = pygame.font.SysFont('arialblack', 17)
    font2 = pygame.font.SysFont('arialblack', 25)
    font3 = pygame.font.SysFont('calibri', 10)
    pygame.time.set_timer(GOING_UP, 3000)

    dy = 0
    going_up = False

    clock = pygame.time.Clock()
    run = True
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == GOING_UP:
                going_up = True
                pygame.time.set_timer(GOING_UP, 0)
            if event.type in [pygame.KEYDOWN, pygame.MOUSEBUTTONDOWN]:
                return start_screen(screen, False, False)

        screen.blit(pygame.image.load('data/background.png'), (0, 0))
        thanks_sur = font2.render(thanks, 1, (255, 255, 0))
        screen.blit(thanks_sur, (20, HEIGHT // 2 - dy))
        for i in range(len(text)):
            screen.blit(font1.render(text[i], 1, (255, 255, 0)), (7, 1.25 * HEIGHT + 55 * i - dy))
        screen.blit(font3.render(endings, 1, (255, 255, 0)), (30, 1.4 * HEIGHT + 45 * 8 + 30 - dy))
        if going_up:
            dy += 30 / FPS

        if dy == 1.4 * HEIGHT + 45 * 8 + 40:
            return start_screen(screen, False, False)
        pygame.display.flip()
        clock.tick(FPS)
