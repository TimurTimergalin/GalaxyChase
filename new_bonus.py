from Bonus import *
import random


def new_bonus(player, enemy, *groups):
    bonuses = [Shield, Bomb]
    i = random.choice(bonuses)
    if random.randint(1, i.chance) == 1 and len(groups[1]) < 1:
        i(player, enemy, *groups)
