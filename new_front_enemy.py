from constant import *
from Ship import *
import random


def new_front_enemy(player, *groups):
    front_enemies = [FrontEnemy]
    for i in front_enemies:
        if random.randint(1, i.chance) == 1 and len(groups[1]) < 6:
            i(player, *groups)