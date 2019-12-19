import pygame


def load_image(name, colorkey=-1):
    fullname = f'data/{name}'
    image = pygame.image.load(fullname)
    if colorkey is not None:
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)

    return image