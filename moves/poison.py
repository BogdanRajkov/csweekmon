"""The implementation of the Poison move.

This move inflicts the Poison status effect. There is no immediate damage, but the opponent will
experience some damage at the start of its every turn until an Antidote is used. The move's
effectiveness is increased the higher the user's Special stat is.
"""

import random
from utils import Printer

NAME = 'Poison'
PP_COST = 5
SUCCESS_RATE = 70
CAN_DISABLE = True

def perform(user, other):
    """Perform Poison."""
    other.stats['Recent damage'] = 0
    if random.randint(0, 99 - user.stats['Special']) > SUCCESS_RATE or \
            'Poison' in other.stats['Effects']:
        Printer.print_ui('  It\'s ineffective!')
    else:
        Printer.print_ui('  {} is now poisoned!'.format(other.name))
        other.stats['Effects'].append('Poison')
        other.stats['Poison Strength'] = max(user.stats['Special'] * 0.5, 8)

def latent(user):
    """The latent influence of the Poison status effect."""
    return random.randint(1, user.stats['Poison Strength'] + 1)
