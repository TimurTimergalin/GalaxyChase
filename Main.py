import pygame
from constant import *
from Ship import *
from new_front_enemy import new_front_enemy
from game import start_screen
pygame.init()
pygame.mixer.init()
size = WIDTH, HEIGHT
screen = pygame.display.set_mode(size, pygame.NOFRAME)
pygame.time.delay(2000)
start_screen(screen)