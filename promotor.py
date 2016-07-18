__author__ = 'brighamhausman'

"""Promotes a character. Need a separatre object because  both the Initator and the Specialmission_boss do that
   and I'm running into a closure error when the SMB which has an initiator (to promotsurviving agents) gets imported
   into the Initiator who needs the SMB for assinging missions to characters."""

from serviceobjectmanager import ServiceObjectManager
from fate import Fate
from random import choice


class Promotor:
    # 1. hook into service data
    __service_obj_mgr = ServiceObjectManager()
    __services = {}
    # 2. dress_out function
    # 3. skill_pick function + supporting functions
    # 4. update_muster function

    def __init__(self):
      self.__services = self.__service_obj_mgr.targ_object_dictionary

    def promote_character(self, character, status):
        # certain services (Other, Scouts, etc) don't have ranks,
        # need to give them bonuses w/o throwing index errors
        service = self.__services[character.service]
        if len(service['ranks']) > 0:
            character.iscommissioned = True # in case they got promoted in a special mission
            status.append(character.name + ' got promoted!')
            character.ranklevel += 1
            new_rank = service['ranks'][character.ranklevel - 1]
            character.militarytitle = new_rank
            status.append(' New rank: ' + new_rank)
        # do promotion bonus here
        # one service skill for promoting
        status.extend(self.dress_out(character))
        status.extend(self.skill_pick(character))
        status.extend(self.update_muster(character))
        return status

    def dress_out(self, character):
        result = ['dressing out character now']
        service = self.__services[character.service]
        """happens when a character gets enlisted, drafted or promoted"""
        res = 'No skills from dress out'
        # check rank and service against ranklevel
        rank_level = character.ranklevel
        rank_and_service = service['rank_and_service_skills']
        if rank_level in rank_and_service:
            res = 'character gained: '
            res += str(rank_and_service[rank_level])
            res += ' from dress out'
            character.add_skill(rank_and_service[rank_level])
        result.append(res)
        return result

    def skill_pick(self, character):
        result = ['picking character skill now']
        """picks skill set, gets skill, adds skill to character"""
        skillset = self.__select_skill_type(character)
        skill = self.__new_skill(character, skillset)
        try:
            character.add_skill(skill)
        except TypeError as tex:
            print('add_skill barfed when it got:', skill)
            raise tex

        skill_info = character.name + ' learned '
        skill_info += skillset + ' --> ' + skill[0]
        result.append(skill_info)
        return result

    def __select_skill_type(self, character):
        service = self.__services[character.service]
        fate = Fate()
        """get all the skills tables, add the second
           advanced skills table if education is 8 or higher
           return one at random"""
        convertme = character.get_chars_map()['education']
        char_value = fate.hex_to_num(convertme)
        is_adv = char_value >= 8
        all_skills = service['aquired_skills']
        eligibile_skills = []
        for skillslist in all_skills:
            if skillslist != 'advanced_education_2':
                eligibile_skills.append(skillslist)
        if is_adv is True:
            eligibile_skills.append('advanced_education_2')
        return choice(eligibile_skills)


    def __new_skill(self, character, skill_type):
        service = self.__services[character.service]
        """picks a new skill from a defined target"""
        available_skills = service['aquired_skills'][skill_type].copy()
        skill = available_skills.popitem()
        return skill[1]

    def update_muster(self,character):
        if(character.ranklevel <= 2):
            character.musterdata['rolls'] += 1
        elif(character.ranklevel == 3 or character.ranklevel == 4):
            character.musterdata['rolls'] += 2
        elif(character.ranklevel == 5 or character.ranklevel == 6):
            character.musterdata['rolls'] += 3
        return ['Character muster roll updated']

if __name__ == '__main__':
    from Character import Character
    p = Promotor()
    c = Character()
    c.service = 'Army'
    outcome = p.promote_character(c, [])
    for item in outcome:
        print(item)