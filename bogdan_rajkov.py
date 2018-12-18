
from actions import Action
from utils import Printer

from game_engine import MOVES, ITEMS
ALL_MOVES_COUNT = len(MOVES)
ALL_ITEMS_COUNT = len(ITEMS)

class TestStrategy:

    def __init__(self):
        self.my_stats = {}
        self.enemy_stats = {}

    @staticmethod
    def set_initial_stats():
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

    @staticmethod
    def set_initial_stats():
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


class PajinStrategy:

    def __init__(self):
        self.stats = {}
        self.enemy_stats = {}
        self.cookies = 2
        self.echoes = 2
        self.restore = 1
        self.first = False

    @staticmethod
    def set_initial_stats():
        return {'Name': 'Pajin',
                'HP': 31,
                'PP': 29,
                'Strength': 0,
                'Defense': 0,
                'Special': 20,
                'Moves': [10, 1, 12],
                'Items': [3, 5, 5, 0, 0]}

    def set_order_info(self, is_first):
        self.first = is_first

    def receive_my_stats(self, own_stats):
        self.stats = own_stats

    def receive_enemy_stats(self, enemy_info):
        self.enemy_stats = enemy_info

    def choose_action(self):
        if self.stats['HP'] <= 12 and self.cookies > 0:
            self.cookies = self.cookies - 1
            return Action.USE_ITEM, (3 + self.cookies)  # COOKIE
        if 'Disable' in self.stats['Effects'] and self.echoes > 0:
            self.echoes = self.echoes - 1
            return Action.USE_ITEM, (1 + self.echoes)  # ECHO SCREEN
        if self.restore != 0 and self.stats['PP'] < 14:
            self.restore = 0
            return Action.USE_ITEM, 0  # PP RESTORE
        if self.stats['PP'] >= 14:
            return Action.PERFORM_MOVE, 0  # BLAZE
        if self.stats['PP'] >= 6:
            return Action.PERFORM_MOVE, 2  # DRAIN
        if self.stats['PP'] >= 5 and 'Poison' not in self.enemy_stats['Effects']:
            return Action.PERFORM_MOVE, 1  # POISON
        return Action.BLOCK, 0

class Day2Strategy:

    def __init__(self):
        self.my_stats = {}
        self.is_first = False
        self.max_cookies = 10
        self.cookies_used = 0
        self.enemy_stats = {}
        self.enemy_moves = []
        self.enemy_items = []

    @staticmethod
    def set_initial_stats():
        return {'Name': 'Debelimon',
                'HP': 0,
                'PP': 0,
                'Strength': 0,
                'Defense': 0,
                'Special': 0,
                'Moves': [8, 2, 0],
                'Items': [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]}

    def set_order_info(self, is_first):
        self.is_first = is_first

    def receive_my_stats(self, own_stats):
        self.my_stats = own_stats

    def receive_enemy_stats(self, enemy_info):
        self.enemy_stats = enemy_info
        if not self.enemy_moves:
            self.enemy_moves = enemy_info['Moves']
        if not self.enemy_items:
            self.enemy_items = enemy_info['Items']

    def choose_action(self):
        pr_disable = (1 - [x in self.enemy_moves and not x.CAN_DISABLE for x in MOVES].count(True)/4) * \
                     ('Disable' not in self.enemy_stats['Effects'])
        pr_attack = 0.5
        pr_heal = (1 - self.my_stats['HP']/self.my_stats['Max HP'])
        decision = [('disable', pr_disable), ('attack', pr_attack), ('heal', pr_heal)]
        decision.sort(key=lambda x: x[1], reverse=True)
        action = decision[0]
        if action == 'disable' and self.my_stats['PP'] >= MOVES[8].PP_COST:
            return Action.PERFORM_MOVE, 0
        if action == 'attack':
            if self.my_stats['PP'] < MOVES[2].PP_COST:
                return Action.PERFORM_MOVE, 2
            base_counter = max(0, 0.5 * self.my_stats['Recent damage']
                                  + self.my_stats['Strength']
                                  - self.my_stats['Defense'])
            base_tackle = max(0, 0.7 * self.my_stats['Strength'] - self.enemy_stats['Defense'])
            if base_counter > base_tackle:
                return Action.PERFORM_MOVE, 1
            else:
                return Action.PERFORM_MOVE, 2
        if action == 'heal' and self.cookies_used < self.max_cookies:
            self.cookies_used += 1
            return Action.USE_ITEM, self.cookies_used - 1
        return Action.BLOCK, 0
