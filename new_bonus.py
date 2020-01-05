from Bonus import Shield
import random


def new_bonus(player, *groups):
    bonuses = [Shield]
    for i in bonuses:
        if random.randint(1, i.chance) == 1 and len(groups[1]) < 1:
            i(player, *groups)
