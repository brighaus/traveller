from fate import Fate as fate
from characterobjectmanager import CharacterObjectManager
from serviceobjectmanager import ServiceObjectManager
from specialmission_boss import Specialmission_boss
from promotor import Promotor
from random import choice
import util.data_config as dbcfg

"""
Goes through a local dir and extracts info from all relevant cfg files.
each cfg represents a possible trade for the Character
to learn/experience
"""


class Initiator(object):
    """Takes a Character object through its initiation lifecycle"""

    def __init__(self, character_object=None):
        self.__data_targs = dbcfg.DB_TARGETS()
        self.__service_object_manager = ServiceObjectManager()
        self.__character_object_manager = CharacterObjectManager()
        self.__special_mission_boss = Specialmission_boss()
        self.__promotor = Promotor()
        self.__character_object = character_object
        self.__service_branches = None
        self.__fate = fate()
        self.__service_data_src = self.__data_targs.service_branches
        self.__service_branch_list = []
        self.__service_file_suffix = 'svc'
        self.__service_name_attr = 'service_name'
        self.__current_service_term = 0
        self.__character_data_src = self.__data_targs.characters
        self.__character_file_suffix = 'chr'

    #service_mgr
    def __load_service_branches(self):
        """fetches names of all available branches in service_branches dir
             [or by name in list passed to self.cfg -- to be built] """
        svcmgr = self.__service_object_manager
        self.__service_branches = svcmgr.targ_object_dictionary
        self.__service_branch_list = svcmgr.object_names_list

    #character_mgr
    def __milestone(self, character, service, goal, mods=[]):
        """(dict, dict, str, list) returns boolean
            use for commission, promotion, etc"""
        chrmgr = self.__character_object_manager
        return chrmgr.milestone(character, service, goal, mods)

    # check_aging

    # TODO: this should be in a manager class.
    # there are various objects that needs this:
    # characters, services, planets, vehicles, etc.
    def create_service_branch(self, branch_data):
        #make path
        file_name = branch_data[self.__service_name_attr]
        file_name += '.' + self.__service_file_suffix
        #file name is
        path = self.__service_data_src + '/' + file_name
        self.__service_object_manager.store(branch_data, path)

        
    def store_character(self, character_obj):
        key = self.__character_object_manager.store(character_obj)
        return key

    def get_character(self, char_key, service):
        """yanks a character from the repo based on key"""
        ret_val = self.__character_object_manager.get_character_from_store(char_key, service)
        return ret_val

    # for referencing the right key in the character status
    def get_current_service_term_key(self):
        cst = self.__current_service_term
        return 'term_' + str(cst)
        

    def service_branch_list(self):
        """ return all available service_branches by name """
        if self.__service_branches is None:
            self.__load_service_branches()
        return self.__service_branch_list

    def prior_service_info(self, service_name):
        """return the prior service table
           from self.__service_branches"""
        return self.__service_branches[service_name]['prior_service']

    def mod_val(self, character_obj, service_obj, look_up):
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
            char_value = self.__fate.hex_to_num(char_value)
            char_value = int(char_value)
        else:
            char_value = 0

        if char_value >= mod_plus_value:
            return_val += bonus

        return return_val

    def enlist(self, character_obj, service_name):
        #status = []
        """ roll for enlistment and return true or false """
        # get service by service name
        servicedata = self.service_data(service_name)
        serviceterm_key = self.get_current_service_term_key()

        # get enlistment cost
        cost = servicedata['prior_service']['enlistment_roll']
        enlist_cost = 'enlistment cost: ' + str(cost)
        character_obj.status[serviceterm_key].append(enlist_cost)
        #get base roll
        self.__fate.set_dice_type('2d6')
        fate_roller = self.__fate
        base_roll = fate_roller.roll()
        character_traits = character_obj.get_chars_map()
        out = ''

        # get mods
        mod_plus_one = servicedata['prior_service']['enlistment_mod_+1_min']
        mod_plus_one_trait = mod_plus_one[0]
        mod_plus_two = servicedata['prior_service']['enlistment_mod_+2_min']
        mod_plus_two_trait = mod_plus_two[0]

        ch_mod_pl_1_val = -1
        if mod_plus_one_trait in character_traits.keys():
            ch_mod_pl_1_val = character_traits[mod_plus_one_trait]

        ch_mod_pl_2_val = -1
        if mod_plus_two_trait in character_traits.keys():
            ch_mod_pl_2_val = character_traits[mod_plus_two_trait]
        out = 'service plus one minimum:' + str(mod_plus_one)
        character_obj.status[serviceterm_key].append(out)
        out = 'service plus two minimum ' + str(mod_plus_two)
        character_obj.status[serviceterm_key].append(out)

        ch_mod_pl_1_val = fate_roller.hex_to_num(ch_mod_pl_1_val)

        if not isinstance(ch_mod_pl_2_val, int):
            ch_mod_pl_2_val = fate_roller.hex_to_num(ch_mod_pl_2_val)

        if int(ch_mod_pl_1_val) >= int(mod_plus_one[1]):
            out = 'character trait: ' + mod_plus_one[0]
            out += ' is greater than min, incrementing'
            base_roll += 1

        if int(ch_mod_pl_2_val) >= int(mod_plus_two[1]):
            out = 'character trait: ' + mod_plus_two[0]
            out += ' is greater than min, incrementing by two'
            base_roll += 2

        character_obj.status[serviceterm_key].append(out)

        outcome = base_roll >= cost

        if outcome is True:
            character_obj.militarytitle = service_name
            dressout = character_obj.name + ' successfully enlisted to: '
            dressout += service_name
            character_obj.update_status(self.get_current_service_term_key(), [dressout])
            character_obj.service = service_name
            dressout = 'enlist dress_out results: '
            character_obj.update_status(self.get_current_service_term_key(), [dressout])
            character_obj.update_status(self.get_current_service_term_key(), self.dress_out(character_obj))
            character_obj.status[serviceterm_key].append(dressout)
        else:
            failed = character_obj.name + ' did not successfully enlist in ' + service_name
            character_obj.update_status(self.get_current_service_term_key(), [failed])

        return outcome

    def draft(self, character):
        """returns a service name, selected at random from the
           serivce_branches list"""
        service_branch_list = self.service_branch_list()
        selected_service = choice(service_branch_list)
        character.militarytitle = selected_service
        character.service = selected_service
        character.service = selected_service
        self.dress_out(character)
        return selected_service

    def increment_service_term(self, character):
        character.termsserved += 1
        self.__current_service_term = character.termsserved


    def doterm(self, character_obj):
        """updates the state of the character object
           based on the outcome of the term,
           returns an array of strings with details of the term"""
        self.increment_service_term(character_obj)
        begin = character_obj.name + ' enters service term '
        begin += str(character_obj.termsserved)
         # get service object based on c.service
        rank = character_obj.militarytitle
        begin += ' ranked as a: ' + rank + '.'
        cst_key = self.get_current_service_term_key()
        character_obj.status[cst_key] = []
        character_obj.status[cst_key].append(begin)
        # reenlist
        if character_obj.termsserved > 1:
            character_obj.status[cst_key].append(character_obj.name + " attempts to reenlist.")
            isretired = self.reenlist(character_obj)
            if isretired is True:
                character_obj.status[cst_key].append('Reenlistment petition denied!')
            else:
                character_obj.status[cst_key].append('Reenlist request honored!')


        isactive = not character_obj.isretired

        if isactive is True:
            # did they get a mission and accept?

            #else did they survive?
            character_obj = self.survive(character_obj)

        if character_obj.isalive is True and isactive is True:

            self.upgrade_for_term(character_obj)

            # # one muster roll per term
            # character_obj.musterdata['rolls'] += 1
            # # one skill per term
            # skill_info = self.do_skill_pick(character_obj)
            # character_obj.status[cst_key].append(skill_info)
            #
            # # scouts get an extra skill
            # if character_obj.service == 'Scouts':
            #     skill_info = self.do_skill_pick(character_obj)
            #     character_obj.status[cst_key].append(skill_info)


            # # one skill for first term
            # if character_obj.termsserved == 1:
            #     skill_info = self.do_skill_pick(character_obj)
            #     character_obj.status[cst_key].append(skill_info)
            #did they get a commission?
            iscommissioned = character_obj.iscommissioned
            if iscommissioned is True:
                # try for promotion
                gotpromoted = self.promotion(character_obj)
                for evt in gotpromoted:
                    character_obj.status[cst_key].append(evt)
            else:
                # try for commission
                comm_result = self.commission(character_obj)
                iscommissioned = character_obj.iscommissioned
                for evt in comm_result:
                    character_obj.status[cst_key].append(evt)
                if iscommissioned is True:
                    # add commission bonus here?
                    # try for promotion
                    promo_result = self.promotion(character_obj)
                    for evt in promo_result:
                        character_obj.status[cst_key].append(evt)

            self.age_for_term(character_obj)

        return character_obj

    def age_for_term(self, character):
        character.age += 4
        age_info = character.name + ' is now age: '
        age_info += str(character.age)
        character.update_status(self.get_current_service_term_key(), [age_info])

    def upgrade_for_term(self, character):
        current_service_term_key = self.get_current_service_term_key()
        # one muster roll per term
        character.musterdata['rolls'] += 1
        # one skill per term
        skill_info = self.do_skill_pick(character)
        character.status[current_service_term_key].append(skill_info)

        # scouts get an extra skill
        if character.service == 'Scouts':
            skill_info = self.do_skill_pick(character)
            character.status[current_service_term_key].append(skill_info)

        # one skill for first term
        if character.termsserved == 1:
            skill_info = self.do_skill_pick(character)
            character.status[current_service_term_key].append(skill_info)

    '''@return dict of service information'''
    def service_data(self, service_name):

        if self.__service_branches is None:
            self.__load_service_branches()

        # get service by service name
        return_data = self.__service_branches[service_name]
        return return_data

    def promotion(self, character):
        # try for promotion
        goal = 'promotion_roll'
        mods = ['promotion_mod_+1_min']
        promo_result = ['Character not eligible for promotion.']
        service = self.service_data(character.service)
        if service['prior_service']['promotion_roll'] > 0:
            promo_result[0] = character.name + " tried for promotion."
            ispromoted = self.__milestone(character,
                                          service,
                                          goal,
                                          mods)
            if ispromoted is True:
                promo_result = self.promote_character(character, promo_result)

            else:
                promo_result.append("Promotion  attempt failed, bummer.")

        return promo_result

    def promote_character(self, character, status):
        return self.__promotor.promote_character(character, status)

    def commission(self, character):
        service = self.service_data(character.service)
         # try for commission
        commish_result = ['Character not eligible for commission.']

        if service['prior_service']['commission_roll'] > 0:
            goal = 'commission_roll'
            mods = ['commission_mod_+1_min']
            commish_result[0] = character.name + " tried for a commission."
            iscommissioned = self.__milestone(character,
                                              service,
                                              goal,
                                              mods)
            if iscommissioned is True:
                character.iscommissioned = True
                commish_result.append(character.name + ' got commissioned!')
                # do comission bonus here
                commish_result.append(self.do_skill_pick(character))
                # one service skill for commission
            else:
                commish_result.append('Attempt failed. Feh.')

        return commish_result

    def reenlist(self, character):
        """tests whether the character reenlists successfully.
            if not, updates character isretired property.
            @return boolean -- True if reenlist is successful"""

        service = self.service_data(character.service)
        # try for reenlist
        if service['prior_service']['reenlist'] > 0:
            goal = 'reenlist'
            isenlisted = self.__milestone(character,
                                          service,
                                          goal)
            if isenlisted is False:
                character.isretired = True

        isretired = character.isretired

        return isretired


    def get_mission_status(self, character):
        """returns a mission object or None"""
        return self.__special_mission_boss.get_character_mission(character)


    # run a character through a mission and update the character's status
    def engage_mission(self, character, mission):
        survived = []
        # return outcome, character, char_status
        mission_result,character,char_status = self.__special_mission_boss.mission_outcome(mission, character)
        survived.extend(mission_result['description'])
        survived.extend(char_status)
        # check for promotions in mission rewards
        self.age_for_term(character)
        character.update_status(self.get_current_service_term_key(), survived)
        return survived

    def survive(self, character):
        survived = []
        service = self.service_data(character.service)
        # get survival cost
        survival_cost = service['prior_service']['survival_roll']
        self.__fate.set_dice_type('2d6')
        base_roll = self.__fate.roll()
        mod = self.mod_val(character, service, 'survival_mod_+2_min')
        mod_roll = base_roll + mod

        #did they survive?
        out = 'To survive, ' + character.name
        out += ' needed to roll: ' + str(survival_cost)
        survived.append(out)
        out = 'Base roll: ' + str(base_roll) + ' plus '
        out += 'a modifier of: ' + str(mod) + ' for character traits'
        survived.append(out)
        if mod_roll < survival_cost:
            character.isalive = False
            survived.append(character.name + ' is DEAD!!!')

        else:
            survived.append(character.name + ' survived this term.')

        character.update_status(self.get_current_service_term_key(), survived)
        return character

    def dress_out(self, character):
        service = self.service_data(character.service)
        result = []
        """happens when a character gets enlisted, drafted or promoted"""
        dressout = 'No skills from dress out'
        # check rank and service against ranklevel
        rank_level = character.ranklevel
        rank_and_service = service['rank_and_service_skills']
        rank_and_service = service['rank_and_service_skills']
        if rank_level in rank_and_service:
            dressout = ''
            dressout += 'character gained: '
            dressout += str(rank_and_service[rank_level])
            dressout += ' from dress out'
            character.add_skill(rank_and_service[rank_level])
        result.append(dressout)
        character.update_status(self.get_current_service_term_key(), result)
        return result

    def select_skill_type(self, character):
        service = self.service_data(character.service)
        """get all the skills tables, add the second
           advanced skills table if education is 8 or higher
           return one at random"""
        convertme = character.get_chars_map()['education']
        char_value = self.__fate.hex_to_num(convertme)
        is_adv = int(char_value) >= 8
        all_skills = service['aquired_skills']
        eligibile_skills = []
        for skillslist in all_skills:
            if skillslist != 'advanced_education_2':
                eligibile_skills.append(skillslist)
        if is_adv is True:
            eligibile_skills.append('advanced_education_2')
        return choice(eligibile_skills)

    def new_skill(self, character, skill_type):
        service = self.service_data(character.service)
        """picks a new skill from a defined target"""
        # roll 1d6
        self.__fate.set_dice_type('1d6')
        base_roll = self.__fate.roll()
        pick_roll = base_roll
        skill = service['aquired_skills'][skill_type][pick_roll]
        return skill

    def do_skill_pick(self, character):
        service = self.service_data(character.service)
        """picks skill set, gets skill, adds skill to character"""
        skillset = self.select_skill_type(character)
        skill = self.new_skill(character, skillset)
        character.add_skill(skill)
        skill_info = character.name + ' learned '
        skill_info += skillset + ' --> ' + skill[0]
        return skill_info

    def updatemuster(self, character):
        if(character.ranklevel == 1 or character.ranklevel == 2):
            character.musterdata['rolls'] += 1
        elif(character.ranklevel == 3 or character.ranklevel == 4):
            character.musterdata['rolls'] += 2
        elif(character.ranklevel == 5 or character.ranklevel == 6):
            character.musterdata['rolls'] += 3

    def musterout(self, character):
        musterinfo = []
        """Muster rules:
                One benefit roll for each term served
                Rank 1 or 2 receives an extra roll
                Rank 3 or 4 receives 2 extra rolls
                Rank 5 or 6 receives 3 extra rolls
                   also gets +1 on rolls against skills/benefits
                Character has Gambling 1+ gets +1 against cash table
                Only 3 cash rolls"""
        servicedata = self.service_data(character.service)
        servicemuster = servicedata['mustering_out']

        iscashroll = False


        rollinfo = character.name + ' has '
        rollinfo += str(character.musterdata['rolls'])
        rollinfo += ' rolls and '

        # if character has cash rolls, do a random pick
        cashrolls = character.musterdata['cashrolls']

        rollinfo += str(cashrolls) + ' cash rolls.'
        musterinfo.append(rollinfo)
        musterinfo.append('getting swag...')

        if cashrolls > 0:
            self.__fate.set_dice_type('1d3')
            # between cash and muster with a
            # 2:1 favor to musterdata
            bene_type_int = self.__fate.roll()
            # if cash gets picked roll for cash,
            # subtract a cash roll and add to char's cash property
            if bene_type_int == 1:
                cashbenefits = servicedata['cash_benefits']
                iscashroll = True
                character.musterdata['rolls'] -= 1
                character.musterdata['cashrolls'] -= 1
                self.__fate.set_dice_type('1d6')
                roll = self.__fate.roll()
                mod = 0
                if 'Gambling' in character.skills.keys():
                    mod += character.skills['Gambling']
                roll += mod
                cashval = cashbenefits[roll]
                musterinfo.append('got ' + str(cashval) + 'credits\n')
                character.cash += cashval

        if(character.musterdata['rolls'] > 0 and
           iscashroll is False):

            # get modifiers
            modplus = 0
            if(character.ranklevel > 5):
                modplus += 1
            # get id6 roll
            self.__fate.set_dice_type('1d6')
            base_roll = self.__fate.roll()
            base_roll += modplus
            item = servicemuster[base_roll]
            musterinfo.append(character.name + ' got:' + str(item))
            #if it's a trait/skill upgrade,
            # add skill to character
            if item[1] > 0:
                character.add_skill(item)

            #else add item
            else:
                #consider checking and incrementing item count...
                if item[0] in character.items.keys():
                    character.items[item[0]] += 1
                else:
                    character.items[item[0]] = 1

            #remove one roll
            character.musterdata['rolls'] -= 1

        character.update_status('Muster Out', musterinfo)
        #character.status['Muster Out'] = musterinfo
        if character.musterdata['rolls'] > 0:
            self.musterout(character)
        return character
