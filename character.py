#!/usr/bin/python
from fate import Fate as fate


class Character():
    """class that generates an character object"""

    #default props
    __characteristics = ['strength',
                         'dexterity',
                         'endurance',
                         'intelligence',
                         'education',
                         'socialstatus']

    __nobletitles = {'B': 'Knight, Knightess, Dame',
                     'C': 'Baron, Baronet, Baroness',
                     'D': 'Marquis, Marquesa, Marchioness',
                     'E': 'Count, Countess',
                     'F': 'Duke, Duchess'}

    def __init__(self):
        self.createdon = "1/1/2301"  # date character created
        self.characteristics = self.__characteristics
        self.name = "Rookie"  # updated after finishing training
        self.UPP = None
        self.chars_map = None
        self.militarytitle = "Fresh Meat"  # rank earned during duty
        self.nobletitle = "Citizen"  # social status in aristocratic terms
        self.birthdate = "1/1/2301"
        self.age = 18
        self.isalive = True

        """ + for drugs, - for sleep,
            format - 'combatdrugs':5, 'recoverystatis': -3"""
        self.agemodifiers = {}
        self.birthworld = "Terra"
        self.service = "Draft Dodger"  # military service or trade
        self.isdrafted = False  # true if they can't enlist
        self.iscommissioned = False  # true to get above rank 0
        self.branch = "Drifters"  # branch of military/trade service
        self.dischargeworld = "Jupiter"  # right in the middle of´ the storm
        self.termsserved = 0
        self.ranklevel = 0
        self.missions = [] #indexes of special missions
        self.isretired = False
        self.cash = 0
        self.items = {}
        self.musterdata = {'rolls': 0, 'cashrolls': 3}
        self.awards = []  # includes decorations from missions
        self.skills = {}  # skill : rating -- {'Vacc Suit': 2, 'Pilot': 1}
        self.weaponpreferences = {'weapon': 'bluster',
                                  'pistol': 'puny derringer',
                                  'blade': 'shiv'}
        self.travellersmember = False
        self.psitestdate = '1/1/2301'  # when tested for psionics
        self.psiPSR = 0
        self.psitrainingcomplete = '1/1/2301'
        self.status = {'term_0': ["Character created..."]}

    def __str__(self):
        return '%s->%s->%s->%s' % (self.__class__.__name__, self.service, self.militarytitle, self.UPP)

    def get_UPP(self):
        """returns a series of characters matching the length of model"""
        # check self.UPP, if is None
        if self.UPP is None:
            self.UPP = ''
            # call random generator to return 2d6 in hex
            ft = fate({'dice': '2d6', 'type': 'hex'})
            for itm in self.characteristics:
                self.UPP += str(ft.roll())
        return self.UPP

    def get_chars_map(self):
        """returns a dictionary that maps self.characteristics and self.UPP"""
        if self.chars_map is None:
            charmap = {}
            cnt = 0
            upp = self.get_UPP()
            for ch in self.characteristics:
                charmap[ch] = upp[cnt]
                cnt += 1
            self.chars_map = charmap
        return self.chars_map

    def set_chars_map(self, char_attrs):
        # takes a dictionary that matches get_chars_map
        # sets values to fate num_to_hex
        # set new map as value for self.chars_map

        pass

    def get_nobletitles(self):
        """returns a dictionary of nobility titles"""
        return self.__nobletitles

    def isnoble(self):
        """returns true if social status is B or better"""
        rv = False
        searchit = ['B', 'C', 'D', 'E', 'F']
        cm = self.get_chars_map()
        if cm['socialstatus'] in searchit:
            rv = True
        return rv

    def update_status(self, key_str, status_lst):
        """checks status dict, updates list @ key or creates a new list @ key"""
        assert isinstance(status_lst, list), 'Character status must be a list.'
        if(key_str in self.status.keys()):
            self.status[key_str].extend(status_lst)
        else:
            self.status[key_str] = status_lst

    def show_status(self):
        for info in sorted(self.status):
            print(info)
            for item in self.status[info]:
                print(item)

    #TODO: change this design, user should be able to pass in an incremental value for skillinfo[1]
    # where skillinfo = ['key', int_value]
    # right now skills and character attributes are differentiated based on the value of
    # skillinfo[1] being zero (increment skill) or not (increment character trait value)
    def add_skill(self, skillinfo):
        """updates character's skills dictionary or their UUP
        based on the skill"""

        if skillinfo[1] == 0:
            try:
            # update skills dict
                if skillinfo[0] in self.skills:
                    self.skills[skillinfo[0]] += 1
                else:
                    # if it's first time in, load to skills name :0
                    self.skills[skillinfo[0]] = 0
            except TypeError as te:
                print(str(te))
                print('skillinfo:', skillinfo)
                print('skills:', self.skills)


        else:
            # update self.chars_map
            # get character value for skillinfo[0]
            ft = fate({})
            char_traits = self.get_chars_map()
            trait_val = 0
            if skillinfo[0] in char_traits:
                trait_val = char_traits[skillinfo[0]]
            trait_val = ft.hex_to_num(trait_val)
            # if < 15 continue
            if trait_val < 15:
                new_val = trait_val + skillinfo[1]
                new_val = ft.num_to_hex(new_val)
                char_traits[skillinfo[0]] = new_val

    def get_skills(self):
        """spit out the skills dict"""
        return self.skills

    def has_skill(self, skill_name, min_val=0):
        """return true if character has skill_name
            and skill_name value is >= min_val"""
        skills_d = self.get_skills()
        outcome = False
        if skill_name in skills_d and skills_d[skill_name] >= min_val:
            outcome = True

        return outcome



    def add_item(self, item_name):
        #adds an item to the items dictionary
        if item_name in self.items.keys():
            self.items[item_name] += 1
        else:
            self.items[item_name] = 1


if __name__ == '__main__':
    from pprint import pprint
    tc = Character()
    tc.UPP = tc.get_UPP()
    print("Character", tc, sep="\n")
    pprint(vars(tc))