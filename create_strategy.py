"""Creates a stub strategy file."""

import re

from csweekmon import Csweekmon
import game_engine
import strategies

PREAMBLE = \
'"""Autogenerated by create_strategy.py"""\n\
\n\
from actions import Action\n\
\n'

STUB_TEXT = \
'class {}_aStrategy:\n\
\n\
    def __init__(self):\n\
        #TODO: implement behaviour\n\
        pass\n\
\n\
    def set_initial_stats(self):\n\
        return {}\n\
\n\
    def set_order_info(self, is_first):\n\
        #TODO: implement behaviour\n\
        pass\n\
\n\
    def receive_my_stats(self, own_stats):\n\
        #TODO: implement behaviour\n\
        pass\n\
\n\
    def receive_enemy_stats(self, enemy_info):\n\
        #TODO: implement behaviour\n\
        pass\n\
\n\
    def choose_action(self):\n\
        #TODO: implement action selection\n\
        return Action.PERFORM_MOVE, 0'


def controlled_string_input(prompt):
    pattern = re.compile('^[A-Za-z]([A-Za-z0-9_])*$')
    while True:
        string_input = input(prompt)
        if pattern.match(string_input):
            break
        print('Invalid name! Should match pattern [A-Za-z]([A-Za-z0-9_])*')
    return string_input


def controlled_int_input(prompt, maximum, minimum=0):
    while True:
        string_input = input(prompt).lower()
        if string_input.isdigit():
            int_input = int(string_input)
            if int_input > maximum or int_input < minimum:
                print('Invalid number! Should be <= {} and >= {}'.format(maximum, minimum))
                continue
            break
        print('Invalid number! Should only have digits')
    return int_input


CONTESTANT_NAME = ''

def strategy_input(suffix):
    # CSWEEKMON_NAME = ''
    CSWEEKMON_NAME = controlled_string_input('Csweekmon name: ')
    CSW = Csweekmon(strategies.RandomStrategy, False)
    CSW.name = CSWEEKMON_NAME
    while True:
        STAT_POINTS = controlled_int_input('Allocated stat points: ', 300)
        CREDITS = controlled_int_input('Allocated credits: ', 1500)
        print(' | 1 HP is worth {} stat points'.format(game_engine.HP_W))
        print(' | 1 PP is worth {} stat points'.format(game_engine.PP_W))
        print(' | 1 Strength is worth {} stat points'.format(game_engine.STR_W))
        print(' | 1 Defense is worth {} stat points'.format(game_engine.DEF_W))
        print(' | 1 Special is worth {} stat points'.format(game_engine.SPEC_W))
        HP = controlled_int_input('HP: ', 150)
        PP = controlled_int_input('PP: ', 150)
        STRENGTH = controlled_int_input('Strength: ', 100)
        DEFENSE = controlled_int_input('Defense: ', 100)
        SPECIAL = controlled_int_input('Special: ', 100)
        MOVES = []
        ITEMS = []
        print('Moves:')
        for idx, move in enumerate(game_engine.MOVES):
            print('  {}) {}    [PP: {}]'.format(idx + 1, move.NAME, move.PP_COST))
        for idx in range(game_engine.MOVE_COUNT):
            MOVES.append(controlled_int_input('Move #{}: '.format(idx + 1),
                                              game_engine.ALL_MOVES_COUNT, 1) - 1)
        print('Items:')
        print('  0) Nothing (no more items)')
        for idx, item in enumerate(game_engine.ITEMS):
            print('  {}) {}    [cost: {}]'.format(idx + 1, item.NAME, item.COST))
        for idx in range(game_engine.MAX_ITEMS):
            NEW_ITEM = controlled_int_input('Item #{}: '.format(idx + 1),
                                            game_engine.ALL_ITEMS_COUNT, 0) - 1
            if NEW_ITEM == -1:
                break
            ITEMS.append(NEW_ITEM)
        CSW.stats['HP'] = HP
        CSW.stats['PP'] = PP
        CSW.stats['Strength'] = STRENGTH
        CSW.stats['Defense'] = DEFENSE
        CSW.stats['Special'] = SPECIAL
        CSW.stats['Moves'] = MOVES
        CSW.stats['Items'] = ITEMS
        CSW.stats['Banned'] = BANNED
        CSW.stats['Replacement'] = REPLACEMENT
        if game_engine.verify(CSW, CREDITS, STAT_POINTS):
            break
        print('Invalid strategy settings!')
    STATS_DICT = {'Name': CSWEEKMON_NAME,
                  'HP': CSW.stats['HP'],
                  'PP': CSW.stats['PP'],
                  'Strength': CSW.stats['Strength'],
                  'Defense': CSW.stats['Defense'],
                  'Special': CSW.stats['Special'],
                  'Moves': CSW.stats['Moves'],
                  'Items': CSW.stats['Items']}
    with open('{}.py'.format(CONTESTANT_NAME.lower()), 'a') as file:
        file.write('\n\n')
        file.write(STUB_TEXT.format(suffix, CSWEEKMON_NAME, STATS_DICT))
    f.close()


if __name__ == '__main__':
    CONTESTANT_NAME = controlled_string_input('Strategy name: ')
    with open('{}.py'.format(CONTESTANT_NAME.lower()), 'w') as f:
        f.write(PREAMBLE)
    f.close()
    strategy_input('a')
    strategy_input('b')
