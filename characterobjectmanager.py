#!/usr/bin/python
from travellerobjectmanager import TravellerObjectManager
from serviceobjectmanager import ServiceObjectManager
import util.data_config as dbcfg
import os, logging


class CharacterObjectManager(TravellerObjectManager):

    def __init__(self):
        TravellerObjectManager.__init__(self)
        self.__dbtargs = dbcfg.DB_TARGETS()
        self.__log_path = dbcfg.LOG_PATH
        self.__serviceObjectManager = ServiceObjectManager()
        self.__character_data_src = self.__dbtargs.characters
        self.__attr_trait_type = 'upp_attr'
        self.__skill_trait_type = 'skill'
        logging.basicConfig(filename=self.__log_path,level=logging.INFO)


    def milestone(self, character, service, goal, mods=[]):
        """(Character, dict, str, list) returns boolean
            use for commission, promotion, etc"""
        roll_mods = {}
        # get cost
        cost = service['prior_service'][goal]
        # get base roll
        self.fate.set_dice_type('2d6')
        base_roll = self.fate.roll()
        final_roll = base_roll
        # get mods
        for mod_def in mods:
            modifier = self.__mod_val(character, service, mod_def)
            roll_mods[mod_def] = modifier
            final_roll += roll_mods[mod_def]
        return final_roll >= cost

    """returns key of object stored in DB"""
    def store(self, character_obj):
        char_key = self.make_storage_key(character_obj)
        # this needs to get created of it does not already exist.
        data_repo = self.__character_data_src + character_obj.service + '_DB'
        # if data repo does not exist, create it
        if not os.path.isfile(data_repo):
            logging.info("DB not found!! now attempting to create: " + data_repo)
            logging.info("from this perspective: " + os.getcwd())
            self.datamule.to_shelf({}, data_repo)
        self.datamule.update_shelf_member(data_repo, char_key, character_obj)
        return char_key

    # returns all characters in a service
    def get_service_members(self, service_name):
        service_db = self.__character_data_src + service_name + '_DB'

        members = self.datamule.from_shelf(service_db)

        return members

    def get_character_from_store(self, key, service):
        data_repo = self.__character_data_src + service +'_DB'
        ret_val = self.datamule.get_shelf_member(data_repo, key)
        return ret_val
    
    def make_storage_key(self, character_obj):
        #miliratytitle->name->UUP
        storage_key = character_obj.militarytitle
        storage_key += '->'
        storage_key += character_obj.name
        storage_key += '->'
        storage_key += character_obj.get_UPP()
        return storage_key



    def __mod_val(self, character_obj, service_obj, look_up):
        """returns int based on character trait vs
           service requirement"""
        bonus = int(look_up[look_up.find('+') + 1])  # use correct naming!
        return_val = 0
        mod_plus_list = service_obj['prior_service'][look_up]
        mod_plus_value = mod_plus_list[1]
        mod_plus_trait = mod_plus_list[0]
        chars_map = character_obj.get_chars_map()
        if mod_plus_trait in chars_map:
            char_value = chars_map[mod_plus_trait]
            char_value = self.fate.hex_to_num(char_value)
            char_value = int(char_value)
        else:
            char_value = 0

        if char_value >= mod_plus_value:
            return_val += bonus

        return return_val

    def chars_by(self, trait_type, trait_name, min_val):
        characters = []
        # min_level - only return characters with that level or higher
        # get list of all services
        services = self.__serviceObjectManager.service_branches
        # loop each service
        for svc in services:
            #get chars in this service
            veterans = self.get_service_members(svc)
            for vet in veterans:
                char_obj = self.get_character_from_store(vet, svc)

                if trait_type == self.__skill_trait_type:
                    # skill search
                    #skill_name is in char.skills list and value is >= min_level?
                    if trait_name in char_obj.skills and char_obj.skills[trait_name] >= min_val:
                        # add to characters
                        # TODO: more scalable to just pass 'vet' which is the char key?
                        characters.append(char_obj)

                    # UPP attr search
                elif trait_type == self.__attr_trait_type:
                    #skill_name is in char.skills list and value is >= min_level?
                    character_UPP = char_obj.get_chars_map()
                    UPP_trait_int_val = self.fate.hex_to_num(character_UPP[trait_name])

                    if UPP_trait_int_val >= min_val:
                        # add to characters
                        # TODO: more scalable to just pass 'vet' which is the char key?
                        characters.append(char_obj)

        return characters

    def get_by_skill(self, skill_name, min_level):
        characters = self.chars_by(self.__skill_trait_type, skill_name, min_level)
        return characters

    def get_by_UUP_attr(self, attr_name, min_level):
        # attr_name found in character.characteristics list
        matches = self.chars_by(self.__attr_trait_type, attr_name, min_level)
        # min_level - only return characters with that level or higher
        return matches



if __name__ == '__main__':
    # self test
    c_om = CharacterObjectManager()
    print('starting manager:', c_om)

    import Character
    import Initiator
    import ServiceObjectManager as som

    s_om = som.ServiceObjectManager()

    c_o = Character.Character()
    i_o = Initiator.Initiator()

    # generate character traits
    print('character UUP:', c_o.get_UPP())

    # draft character into service
    i_o.draft(c_o)
    character_status = ['character drafted as: ' + c_o.service]
    c_o.update_status('term_0', character_status)

    character_status = i_o.promote_character(c_o, [])
    c_o.update_status('test_promotion', character_status)
    c_o.show_status()


    print('storage key test:', c_om.make_storage_key(c_o))

    # test 'by skill' fetch
    skill = 'Brawling'
    required_level = 0
    matches = c_om.get_by_skill(skill, required_level)
    print('number of characters with', skill ,'minimum skill level of', required_level)
    print(len(matches))

    # test by UPP attribute
    import random
    attrs = c_o.get_chars_map()
    test_attr = random.choice(list(attrs))
    test_minimum = 10
    matches = c_om.get_by_UUP_attr(test_attr, test_minimum)
    print('number of characters with', test_attr, 'minimum value', test_minimum)
    print(len(matches))