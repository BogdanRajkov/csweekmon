"""A few default strategies."""

import random

from actions import Action

class SimpleStrategy:

    def __init__(self):
        self.used_cookies = 0
        self.own_stats = {}
        self.enemy_stats = {}

    def set_initial_stats(self):
        return {'Name': 'Simple',
                'HP': 37,
                'PP': 17,
                'Strength': 10,
                'Defense': 5,
                'Special': 8,
                'Moves': [0, 1, 3],
                'Items': [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                'Banned': 10,
                'Replacement': 9}

    def set_order_info(self, is_first):
        pass

    def receive_my_stats(self, own_stats):
        self.own_stats = own_stats

    def receive_enemy_stats(self, enemy_info):
        self.enemy_stats = enemy_info

    def choose_action(self):
        if self.own_stats['HP'] <= 10 and self.used_cookies <= 10:
            self.used_cookies += 1
            return Action.USE_ITEM, self.used_cookies - 1
        if 'Sleep' not in self.enemy_stats['Effects'] and self.own_stats['PP'] >= 6 \
                and self.own_stats['Moves'][2] == 3:
            return Action.PERFORM_MOVE, 2
        if 'Poison' not in self.enemy_stats['Effects'] and self.own_stats['PP'] >= 5 \
                and self.own_stats['Moves'][1] == 1:
            return Action.PERFORM_MOVE, 1
        if 9 in self.own_stats['Moves'] and self.enemy_stats['Defense'] >= 10:
            return Action.PERFORM_MOVE, self.own_stats['Moves'].index(9)
        return Action.PERFORM_MOVE, 0

class TankStrategy:

    def __init__(self):
        self.turn = 2
        self.stats = {}

    def set_initial_stats(self):
        return {'Name': 'Tank',
                'HP': 50,
                'PP': 10,
                'Strength': 8,
                'Defense': 8,
                'Special': 4,
                'Moves': [4, 0, 0],
                'Items': [],
                'Banned': 1,
                'Replacement': 9}

    def set_order_info(self, is_first):
        pass

    def receive_my_stats(self, own_stats):
        self.stats = own_stats

    def receive_enemy_stats(self, enemy_info):
        pass

    def choose_action(self):
        if self.turn > 0:
            self.turn -= 1
            return Action.PERFORM_MOVE, 0
        return Action.PERFORM_MOVE, 1

class HugePowerStrategy:

    def __init__(self):
        self.stats = {}
        self.enemy_stats = {}
        self.cookies_left = 10

    def set_initial_stats(self):
        return {'Name': 'Huge Power',
                'HP': 35,
                'PP': 35,
                'Strength': 0,
                'Defense': 5,
                'Special': 10,
                'Moves': [6, 10, 12],
                'Items': [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                'Banned': 8,
                'Replacement': 3}

    def set_order_info(self, is_first):
        pass

    def receive_my_stats(self, own_stats):
        self.stats = own_stats

    def receive_enemy_stats(self, enemy_info):
        self.enemy_stats = enemy_info

    def choose_action(self):
        if self.enemy_stats['Previous move'] == 'Focus':
            return Action.BLOCK, 0
        if self.stats['HP'] <= 15:
            if self.stats['PP'] >= 6 and self.stats['Moves'][2] == 12:
                return Action.PERFORM_MOVE, 2
            if self.cookies_left > 0:
                self.cookies_left -= 1
                return Action.USE_ITEM, self.cookies_left
        if self.stats['PP'] >= 14 and self.stats['Moves'][1] == 10:
            return Action.PERFORM_MOVE, 1
        if self.stats['PP'] >= 8 and self.stats['Moves'][0] == 6:
            return Action.PERFORM_MOVE, 0
        if self.stats['PP'] >= 6 and 3 in self.stats['Moves']:
            return Action.PERFORM_MOVE, self.stats['Moves'].index(3)
        return Action.BLOCK, 0

class GlassCannonStrategy:

    def __init__(self):
        self.stats = {}
        self.enemy_stats = {}

    def set_initial_stats(self):
        return {'Name': 'Glass Cannon',
                'HP': 30,
                'PP': 30,
                'Strength': 5,
                'Defense': 5,
                'Special': 10,
                'Moves': [0, 1, 6],
                'Items': [],
                'Banned': 13,
                'Replacement': 12}

    def set_order_info(self, is_first):
        pass

    def receive_my_stats(self, own_stats):
        self.stats = own_stats

    def receive_enemy_stats(self, enemy_info):
        self.enemy_stats = enemy_info

    def choose_action(self):
        if self.enemy_stats['Previous move'] == 'Focus':
            return Action.BLOCK, 0
        if self.stats['PP'] >= 6 and self.stats['HP'] < 15 and 12 in self.stats['Moves']:
            return Action.PERFORM_MOVE, self.stats['Moves'].index(12)
        if self.stats['PP'] >= 26 and self.stats['Moves'][1] == 1:
            return Action.PERFORM_MOVE, 1
        if self.stats['PP'] >= 8 and self.stats['Moves'][2] == 6:
            return Action.PERFORM_MOVE, 2
        if self.stats['PP'] < 5:
            if random.randint(0, 1) == 0:
                return Action.BLOCK, 0
        return Action.PERFORM_MOVE, 0

class RandomStrategy:

    def __init__(self):
        pass

    def set_initial_stats(self):
        return {'Name': 'Random',
                'HP': 32,
                'PP': 12,
                'Strength': 15,
                'Defense': 5,
                'Special': 8,
                'Moves': [0, 1, 2],
                'Items': [],
                'Banned': 3,
                'Replacement': 11}

    def set_order_info(self, is_first):
        pass

    def receive_my_stats(self, own_stats):
        pass

    def receive_enemy_stats(self, enemy_info):
        pass

    def choose_action(self):
        return Action.PERFORM_MOVE, random.randint(0, 2)

class HeavyHitStrategy:

    def __init__(self):
        self.used_kits = 0
        self.used_cookies = 0
        self.used_power = 0
        self.stats = {}
        self.enemy_stats = {}

    def set_initial_stats(self):
        return {'Name': 'Heavy Hit',
                'HP': 60,
                'PP': 10,
                'Strength': 15,
                'Defense': 0,
                'Special': 0,
                'Moves': [0, 2, 7],
                'Items': [1, 0, 2],
                'Banned': 10,
                'Replacement': 13}

    def set_order_info(self, is_first):
        pass

    def receive_my_stats(self, own_stats):
        self.stats = own_stats

    def receive_enemy_stats(self, enemy_info):
        self.enemy_stats = enemy_info

    def choose_action(self):
        if self.stats['HP'] <= 20:
            if self.used_kits < 1:
                self.used_kits += 1
                return Action.USE_ITEM, 0
            if self.used_cookies < 1:
                self.used_cookies += 1
                return Action.USE_ITEM, 1
        if self.used_power < 1:
            self.used_power += 1
            return Action.USE_ITEM, 2
        if self.enemy_stats['PP'] >= 12 and 13 in self.stats['Moves'] and self.stats['PP'] >= 4:
            return Action.PERFORM_MOVE, self.stats['Moves'].index(13)
        if self.stats['PP'] >= 5 and self.stats['Recent damage'] >= 10 \
                and self.stats['Moves'][1] == 2:
            return Action.PERFORM_MOVE, 1
        if self.stats['PP'] >= 4 and self.stats['Moves'][2] == 7:
            return Action.PERFORM_MOVE, 2
        if self.stats['Moves'][0] == 0:
            return Action.PERFORM_MOVE, 0
        return Action.BLOCK, 0