__author__ = 'brighamhausman'
from specialmission import Specialmission
from util import datamule as dm
from util import data_config as dc
from fate import Fate
from promotor import Promotor
import uuid
import logging
"""
Lets you manipulate special assignment db:
    1. create an assignment and store it in the DB
    2. Get a list of eligible assignments based in service
    3. get an assignment for a character
    4. modify the survival roll
    4. determine if the character is successful in the mission
    5. Distribute reward/failure costs to character
    6. check to see if a character survived
    7. check to see if a character failed

"""

class Specialmission_boss(object):

    __repo = None
    __missions_cache = None
    __logging_target = dc.LOG_PATH


    def __init__(self):
        self.__dbs = dc.DB_TARGETS()
        self.__repo = self.__dbs.missions
        #kick off logging
        logging.basicConfig(filename=self.__logging_target,level=logging.DEBUG)


    # stores special mission objects to target repo
    def store_missions(self, special_missions):
        dm.to_shelf(special_missions, self.repo)


    def store_mission(self, special_mission, mission_id=str(uuid.uuid4())):
        special_mission.db_id = mission_id
        dm.update_shelf_member(self.repo, mission_id, special_mission)
        return mission_id

    def modify_character(self, character, mission, outcome):
        mods = {}
        status = []
        if outcome is True:
            mods = mission.reward_package
        else:
            mods = mission.failure_cost

        for mod in mods:
            cache = mods[mod]
            print('mod', mod)
            if mod == 'skills':
                for skill in cache:
                    x = cache[skill]
                    while x > 0:
                        character.add_skill([skill, 0])
                        x -= 1

            if mod == 'attributes':
                for attr in cache:
                    try:
                        attr_name = attr
                        cycles = mods[mod][attr]
                        for cycle in range(cycles):
                            character.add_skill([attr_name, 1])
                    except TypeError as terr:
                        print('wrong format', attr, 'should be [string, int] found', type(attr))


            if mod == 'cash':
                character.cash += cache

            if mod == 'decorations':
                character.awards.append(cache)

            if mod == 'items':
                for item in cache:
                    x = cache[item]
                    while x > 0:
                        character.add_item(item)
                        x -= 1

            if mod == 'promotion':
                promotor = Promotor()
                x = mods[mod]
                while x > 0:
                    status.extend(promotor.promote_character(character, []))
                    x -= 1
        return status

    def modify_survival_roll(self, mission, character):
        # get the mission survival details
        reqs = mission.mission_requirements
        mod = 0
        mod_trace = [] # for debug
        # mod for terms
        if 'terms' in reqs:
            # req_terms - char_terms = modifyer
            mod = reqs['terms'] - character.termsserved
            mod_trace.append('modifier for terms: ' +  str(mod))
        # mod for attributes
        if 'attributes' in reqs:
            req_attr_map = reqs['attributes']
            char_attr_map = character.get_chars_map()
            for ra in req_attr_map:
                attr_mod = 0
                if ra in char_attr_map:
                    mod_trace.append('ra: ' + ra)
                    mod_trace.append('req: ' + str(req_attr_map[ra]))
                    mod_trace.append('char: ' + str(char_attr_map[ra]))
                    # need hex support for this mod
                    fate = Fate()
                    char_attr_num = 0
                    req_attr_num = 0
                    try:
                        char_attr_num = int(char_attr_map[ra])
                    except ValueError as vex:
                        char_attr_num = fate.hex_to_num(char_attr_map[ra])

                    try:
                        req_attr_num = int(req_attr_map[ra])
                    except ValueError as vex:
                        req_attr_num = fate.hex_to_num(req_attr_map[ra])

                    attr_mod += (req_attr_num - char_attr_num)
                    mod_trace.append('attribute mod: ' + str(attr_mod))


                mod += attr_mod
        # mod for skills
        if 'skills' in reqs:
            skills_mod = 0
            char_skills = character.get_skills()
            mod_trace.append('character skills: ' + str(char_skills))
            for skill in reqs['skills']:
                if skill in char_skills:
                    # mod -1 to survival roll for meeting req,
                    skills_mod -= 1
                    # mod -1 for each level over req
                    mod_val = reqs['skills'][skill] - char_skills[skill]
                    mod_trace.append('adjusting ' + str(mod_val) + ' for skill ' + str(skill))
                    skills_mod += mod_val
            mod_trace.append('final skill adjustment: ' + str(skills_mod))
            mod += skills_mod


        mod_trace.append('modifying survival by: ' + str(mod))
        mission.survival_roll += mod
        return mission, mod_trace

    # returns a mission object from the repo w/ outcomes
    # modified based on character traits
    def get_character_mission(self, character):
        # open the db and get a random mission
        mission = None
        # check filters - service
        if bool(self.mission_cache) is True:
            (test_item_id, test_item_details) = self.mission_cache.popitem()

            # already attempted this mission
            if test_item_id in character.missions:
                return None
            if len(test_item_details.services) == 0 or character.service in test_item_details.services:
                # set survival chances
                (modified_mission, debug) = self.modify_survival_roll(test_item_details, character)
                # add survival % for character here and add it as a mission attr
                modified_mission.survival_pct = self.survival_chances(modified_mission, character)
                # return to sender
                mission = modified_mission

        else:
            pass
            # log warning
            #raise Exception('no mission cache!')

        return mission

    # returns a single SM object
    def get_mission(self, mission_id):
        mission = dm.get_shelf_member(self.repo, mission_id)
        return mission

    # get a list if eligible missions based on character
    def get_possible_missions(self, character):
        pass

    def survival_chances(self, mission, character):
        # determines char survival chances based on mission requirements and character traits
        # returns a percentage to survive
        pass

    # returns a dictionary with the details of the mission outcome
    def mission_outcome(self, special_mission, character):
        outcome = {'status': 'SUCCESS', # SUCCESS or FAIL
                   'description': ['you did it!'] # some description of outcome pulled from the mission object
        }

        # add to characters list of attempted missions
        character.missions.append(special_mission.db_id)

        # get a fate object to roll the outcome of 2d6,
        fate = Fate()
        fate.set_dice_type('2d6')
        base_roll = fate.roll()
        logging.info('mission survival::base roll: ' + str(base_roll))
        logging.info('mission survival::survival roll: ' + str(special_mission.survival_roll))
        result = base_roll > special_mission.survival_roll
        # if it's greater than special_mission.survival_roll
        if result is True:
            # they survive, return survivor modified character and outcome
            outcome['status'] = 'SUCCESS'
            outcome['description'] = special_mission.success_description

        # otherwise, they roll to see if they fail or die
        else:
            fate.set_dice_type('1d100')
            fate_score = fate.roll()

            # 50 / 50 chance
            survival_tolerance = 50
            # gamblers can cheat death: survival_tolerance - 5 per level of gambling skill
            gambling_skill_name = 'Gambling'
            logging.info('mission boss checking gambler...')
            if character.has_skill(gambling_skill_name):
                logging.info('mission boss found a gambler')
                survival_tolerance -= 5 * character.get_skills()[gambling_skill_name]

            is_dead = fate_score >= survival_tolerance

            # if they die, return a dead character, modified for fail and outcome
            if is_dead is True:
               character.isalive = False
               outcome['status'] = 'FAIL'
               outcome['description'] = [character.name + " was killed attempting this mission."]
            else:
                # if they fail return modified character and outcome
                outcome['status'] = 'FAIL'
                outcome['description'] = special_mission.fail_description
        char_status = self.modify_character(character, special_mission, result)
        return outcome, character, char_status


    @property
    def repo(self):
        return self.__repo

    @repo.setter
    def repo(self, path):
        self.__repo = path

    @property
    def mission_cache(self):
        if self.__missions_cache is None:
            self.__missions_cache = dm.from_shelf(self.repo)
        return self.__missions_cache


if __name__ == '__main__':
    import os
    from character import Character
    smb = Specialmission_boss()
    smb.repo = 'boss_storage_test'
    if os.path.isfile(smb.repo):
        os.remove(smb.repo)
    character = Character()
    spec_mish_config = {'description':          'this is description by config',
                        'survival_roll':        1,
                        'services':             ['Army', 'Scouts'],
                        'title':                'Boss Special Mission',
                        'reward_package':       {'cash':        50000,
                                                 'skills':      {'Computer': 1, 'Charm': 2},
                                                 'items':       {'Data card': 1, 'Stim shooter': 2},
                                                 'attributes':  {'dexterity', 2},
                                                 'promotion':   1,
                                                 'decorations': ['honorable jabberwock ribbon','octopus tattoo']},
                        'failure_cost':         {'cash':         -500,
                                                 'attributes':   {'intelligence', -1},
                                                 'decorations':  ['cited for being a general dumbass']},
                        'mission_requirements': {'attributes' : {'intelligence': 5},
                                                 'terms':        3,
                                                 'skills': {'Brawling': 0, 'Pilot': 0}}
    }
    spec_mish = Specialmission(spec_mish_config)
    print('this is spec_mish:')
    print('description:', spec_mish.description)
    print('services:', spec_mish.services)
    print('survival roll:', spec_mish.survival_roll)
    print('title:', spec_mish.title)
    print('rewards:', spec_mish.reward_package)
    print('failure cost:', spec_mish.failure_cost)
    print('mission_requirements:', spec_mish.mission_requirements)
    print('saving special mission')
    mish_id = smb.store_mission(spec_mish)
    print('mission id is:', mish_id)
    print('fetching mission from repo...')
    mish_from_repo = smb.get_mission(mish_id)
    print('mission from repo details:', dir(mish_from_repo))
    print('fetching mission for character:')
    character.service = 'Army'
    character.add_skill(['Brawling',0])
    # add_skill increments named skill by one point
    character.add_skill(['Brawling',0])
    character.add_skill(['Pilot', 0])
    character.termsserved = 2
    char_mish = smb.get_character_mission(character)
    print('mission info:', char_mish)
    if char_mish is not None:
        print('modified survival roll:', char_mish.survival_roll)
        char_mish.success_description = ['Things went well!',
                                         character.name + ' got cash, items and some other stuff']
        char_mish.fail_description = ['Bad news!',
                                      'A snitch on the inside set up ' + character.name ,
                                      ' and a bad beating ensued, loss of brain power and cash due to medical bills for starters...']
        (mish_out, character, character_status) = smb.mission_outcome(char_mish, character)
        print('mission status:', mish_out['status'])
        print('mission outcome description:')
        for ln in mish_out['description']:
            print(ln)
        print('character items:', character.items)
        print('character rank', character.militarytitle)
        print('character status change from mission:')
        for sts in character_status:
            print(sts)
    else:
        print('no eligible missions this term')

    if os.path.isfile(smb.repo):
        os.remove(smb.repo)

