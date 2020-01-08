import pygame
from constant import *
from game import *
pygame.init()
pygame.mixer.init()
size = WIDTH, HEIGHT
screen = pygame.display.set_mode(size, pygame.NOFRAME)
pygame.time.delay(2000)
start_screen(screen)
