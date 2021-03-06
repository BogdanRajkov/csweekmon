"""The implementation of the Kick move.

The most basic physical attack. It costs nothing and has no special side effects."""

import random
from utils import Printer

NAME = 'Kick'
PP_COST = 0
SUCCESS_RATE = 90
CRIT_RATE = 15
CAN_DISABLE = False

def perform(user, other):
    """Perform Kick."""
    if random.randint(0, 99) < SUCCESS_RATE:
        if random.randint(0, 99) < CRIT_RATE:
            Printer.print_ui('  It\'s super effective!')
            Printer.delay_ui(1)
            base_damage = max(0, 0.8 * user.stats['Strength'] - 0.1 * other.stats['Defense'])
        else:
            base_damage = max(0, 0.6 * user.stats['Strength'] - 0.2 * other.stats['Defense'])
        damage = max(1, random.randint(int(0.8 * base_damage), int(1.2 * base_damage) + 1))
        if damage == 1:
            Printer.print_ui('  It deals {} point of damage.'.format(damage))
        else:
            Printer.print_ui('  It deals {} points of damage.'.format(damage))
        other.stats['Recent damage'] = damage
        other.stats['HP'] -= damage
    else:
        Printer.print_ui('  It\'s ineffective!')
