from Ship import *
import random


def new_front_enemy(player, bullets, *groups):
    front_enemies = [FrontEnemy, Kamikaze, Giant]
    i = random.choice(front_enemies)
    if random.randint(1, i.chance) == 1 and len(groups[1]) < 6:
        i(bullets, player, *groups)