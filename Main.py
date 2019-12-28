import pygame
from constant import *
from Ship import *
from new_front_enemy import new_front_enemy
from game import *
pygame.init()
pygame.mixer.init()
pygame.time.delay(2000)
size = WIDTH, HEIGHT
screen = pygame.display.set_mode(size)
start_screen(screen)