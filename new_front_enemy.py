from Ship import FrontEnemy
import random


def new_front_enemy(player, *groups):
    if random.randint(1, 50) == 1 and len(groups) < 6:
        FrontEnemy(player, *groups)