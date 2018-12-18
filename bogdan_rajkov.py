
import random

from actions import Action
from utils import Printer

from game_engine import MOVES, ITEMS, MOVE_COUNT, MAX_ITEMS, MAX_COST, STAT_POINTS
from game_engine import HP_W, PP_W, STR_W, DEF_W, SPEC_W
ALL_MOVES_COUNT = len(MOVES)
ALL_ITEMS_COUNT = len(ITEMS)

class TestStrategy:

    def __init__(self):
        self.my_stats = {}
        self.enemy_stats = {}

    def set_initial_stats(self):
        return {'Name': 'Bobo',
                'HP': 40,
                'PP': 30,
                'Strength': 0,
                'Defense': 5,
                'Special': 10,
                'Moves': [1, 3, 10],
                'Items': [0, 0, 3, 4, 5]}

    def set_order_info(self, is_first):
        pass

    def receive_my_stats(self, own_stats):
        self.my_stats = own_stats

    def receive_enemy_stats(self, enemy_info):
        self.enemy_stats = enemy_info

    def choose_action(self):
        Printer.print_ui('***********************************')
        Printer.print_ui('        Choose Action')
        Printer.print_ui('Options:')
        for i in range(len(self.my_stats['Moves'])):
            move = self.my_stats['Moves'][i]
            Printer.print_ui(' * \'move {}\' - Perform {}'.format(i, MOVES[move].NAME))
        for i, item in enumerate(self.my_stats['Items']):
            if item != -1:
                Printer.print_ui(' * \'item {}\' - Use {}'.format(i, ITEMS[item].NAME))
        Printer.print_ui(' * \'block\'  - Perform Block')

        while True:
            inp = input()
            if inp == 'block':
                return Action.BLOCK, 0

            inp = inp.split(' ')

            if len(inp) == 2 and inp[1].isdigit():
                if inp[0] == 'move':
                    return Action.PERFORM_MOVE, int(inp[1])
                if inp[0] == 'item':
                    return Action.USE_ITEM, int(inp[1])
            Printer.print_ui('Invalid command!')

class Day1Strategy:

    def __init__(self):
        self.my_stats = {}
        self.enemy_stats = {}
        # self.enemy_base_defence = 0
        self.prev_HP = 0
        self.in_hurry = False
        self.turn = 0
        self.medkit_used = False
        self.pp_used = False
        self.antidote_used = False
        self.echoscreen_used = False

    def set_initial_stats(self):
        return {'Name': 'Ćtvimon',
                'HP': 40,
                'PP': 30,
                'Strength': 0,
                'Defense': 5,
                'Special': 10,
                'Moves': [1, 3, 10],
                'Items': [1, 3, 4]}

    def set_order_info(self, is_first):
        pass

    def receive_my_stats(self, own_stats):
        self.my_stats = own_stats
        for key in own_stats:
            Printer.print_ui(key+': '+str(own_stats[key]))

    def receive_enemy_stats(self, enemy_info):
        self.enemy_stats = enemy_info
        for key in enemy_info:
            Printer.print_ui(key+': '+str(enemy_info[key]))

    def choose_action(self):
        # if self.turn == 0 or self.enemy_stats['Defence'] < self.enemy_base_defence:
        #    self.enemy_base_defence = self.enemy_stats['Defence']
        if self.turn == 0:
            self.prev_HP = self.my_stats['HP']
        self.turn += 1
        if self.turn > 20 or self.enemy_stats['Previous move'] == 'Focus':
            self.in_hurry = True
        if self.enemy_stats['Strength'] >= 10 and \
            (self.enemy_stats['Previous move'] == 'Focus' or self.my_stats['HP'] < 20):
            self.prev_HP = self.my_stats['HP']
            return Action.BLOCK, 0
        if self.my_stats['HP'] < 12:
            if not self.medkit_used:
                self.medkit_used = True
                self.prev_HP = self.my_stats['HP']
                return Action.USE_ITEM, 0
            if self.my_stats['PP'] < 14:
                self.prev_HP = self.my_stats['HP']
                return Action.BLOCK, 0
        if self.prev_HP - self.my_stats['HP'] > 10 and self.enemy_stats['PP'] >= 14 and self.my_stats['PP'] >= 14:
            self.prev_HP = self.my_stats['HP']
            return Action.PERFORM_MOVE, 2
        if 'Poison' in self.my_stats['Effects'] and not self.antidote_used:
            self.antidote_used = True
            self.prev_HP = self.my_stats['HP']
            return Action.USE_ITEM, 2
        if self.my_stats['PP'] < 3 and not self.pp_used:
            self.pp_used = True
            self.prev_HP = self.my_stats['HP']
            return Action.USE_ITEM, 1
        if 'Poison' not in self.enemy_stats['Effects']:
            if self.my_stats['PP'] >= 5:
                self.prev_HP = self.my_stats['HP']
                return Action.PERFORM_MOVE, 0
            else:
                if self.in_hurry and not self.pp_used:
                    self.pp_used = True
                    self.prev_HP = self.my_stats['HP']
                    return Action.USE_ITEM, 1
                else:
                    self.prev_HP = self.my_stats['HP']
                    return Action.BLOCK, 0
        if self.my_stats['PP'] >= 14:
            self.prev_HP = self.my_stats['HP']
            return Action.PERFORM_MOVE, 2
        if 'Sleep' not in self.enemy_stats['Effects']:
            if self.my_stats['PP'] >= 6:
                self.prev_HP = self.my_stats['HP']
                return Action.PERFORM_MOVE, 1
            else:
                if self.in_hurry and not self.pp_used:
                    self.prev_HP = self.my_stats['HP']
                    return Action.USE_ITEM, 1
                else:
                    self.prev_HP = self.my_stats['HP']
                    return Action.BLOCK, 0
        # if self.enemy_stats['Defense'] > self.enemy_base_defence and not self.in_hurry:
        #    return Action.BLOCK, 0
        if self.my_stats['PP'] < 14 and (not self.in_hurry or self.pp_used):
            self.prev_HP = self.my_stats['HP']
            return Action.BLOCK, 0
        elif self.my_stats['PP'] < 14 and not self.pp_used:
            self.pp_used = True
            self.prev_HP = self.my_stats['HP']
            return Action.USE_ITEM, 1
        self.prev_HP = self.my_stats['HP']
        return Action.PERFORM_MOVE, 2
