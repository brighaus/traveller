#!/usr/bin/python
import random


class Fate():
    __top_vals = {10: 'A',
                  11: 'B',
                  12: 'C',
                  13: 'D',
                  14: 'E',
                  15: 'F'}

    __top_hex_to_num = {'A': 10,
                        'B': 11,
                        'C': 12,
                        'D': 13,
                        'E': 14,
                        'F': 15}

    """Fate rolls dice and returns decimal or hexidecimal values"""
    def __init__(self, cfg={}):
        self.type = 'dec'
        if cfg:
            for prop in cfg:
                if prop == 'dice':
                    self.dice = cfg[prop]
                if prop == 'type':
                    """number type. ex: int vs hexidecimal"""
                    self.type = cfg[prop]

    def roll(self):
        """rolls and returns a value based on self.dice"""

        dice_sides = str.split(self.dice, 'd')
        numdice = int(dice_sides[0])
        sides = int(dice_sides[1])
        retval = random.randrange(numdice, numdice * sides)
        # if cfg.type = hex, hexify
        if self.type and self.type == 'hex':
            # 0-9 are normal
            if retval > 9:
                # 10 - 15 A - F
                retval = self.__top_vals[retval]
        return retval

    def hex_to_num(self, char):
        if char in self.__top_hex_to_num:
            return int(self.__top_hex_to_num[char])
        else:
            return int(char)

    def num_to_hex(self, num):
        if num <= 9:
            return num
        else:
            for hx in self.__top_hex_to_num:
                if self.__top_hex_to_num[hx] == num:
                    return hx

    def dice(self):
        return self.dice

    """roll_type string
        format: xdy
        where x is num dice
        and d is a delimiter
        and y is number of sides"""
    def set_dice_type(self, roll_type):
        self.dice = roll_type

    def set_number_type(self, number_type):
        """sets type of number: integer, hexidecimal, etc"""
        pass
