"""
Object that  can give the user the option to let their character to take on a special assignment. It will be delivered w/ a brief description, a reward for success and a probablity of success.
    1. storage for assignment details
    2. random pick after reenlist
    3. user pick to take it
        - % to survive
        - what could be won
    4. save assignment details onto character

Should have a way to CRUD an assignment, maybe an SA manager class:
 create assignment
 delete
 read
 edit
"""

class Specialmission(object):
    __description = '' # detailed synopsis
    __title = '' # brief description
    __services = [] # services that can be offered this mission, None == any service
    __survival_roll = 0 # what character needs to survive the mission
    __reward_package = {} # what they get if they survive
    __failure_cost = {} # character does not die, but does not succeed either,
                        # test for failure if the character fails survival roll
    __mission_requirements = {'skills': {},
                              'terms': 0,
                              'attributes': {}
                             }# required traits could be # terms, rank (not supported),
                              # certain skill'/skill level, minimum personal trait, etc.
    __success_description = ['Mission accomplished!'] # what the read on success
    __fail_description = ['Mission attempt failed!'] # what they see of the mission fails
    __db_id = '' #set when uuid gets generated

    def __init__(self, config=None):
        if config is not None:
            if 'description' in config:
                self.description = config['description']
            if 'services' in config:
                self.services = config['services']
            if 'survival_roll' in config:
                self.survival_roll = config['survival_roll']
            if 'reward_package' in config:
                self.reward_package = config['reward_package']
            if 'title' in config:
                self.title =  config['title']
            if 'failure_cost' in config:
                self.failure_cost = config['failure_cost']
            if 'mission_requirements' in config:
                self.mission_requirements = config['mission_requirements']
            if 'success_description' in config:
                self.success_description = config['success_description']
            if 'fail_description' in config:
                self.fail_description = config['fail_description']


    #TODO: assert data types
    @property
    def description(self):
        return self.__description

    @description.setter
    def description(self, val):
        self.__description = val

    @property
    def services(self):
        return self.__services

    @services.setter
    def services(self, serviceslist):
        self.__services = serviceslist

    @property
    def survival_roll(self):
        return self.__survival_roll

    @survival_roll.setter
    def survival_roll(self, roll_val):
        self.__survival_roll = roll_val

    @property
    def title(self):
        return self.__title

    @title.setter
    def title(self, title):
        self.__title = title

    @property
    def reward_package(self):
        return self.__reward_package

    @reward_package.setter
    def reward_package(self, rewards):
        self.__reward_package = rewards

    @property
    def failure_cost(self):
        return self.__failure_cost

    @failure_cost.setter
    def failure_cost(self, cost_config):
        self.__failure_cost = cost_config

    @property
    def mission_requirements(self):
        return self.__mission_requirements

    @mission_requirements.setter
    def mission_requirements(self, mission_requirements):
        self.__mission_requirements = mission_requirements

    @property
    def success_description(self):
        return self.__success_description

    @success_description.setter
    def success_description(self, description_list):
        self.__success_description = description_list

    @property
    def fail_description(self):
        return self.__fail_description

    @fail_description.setter
    def fail_description(self, description_list):
        self.__fail_description = description_list

    @property
    def db_id(self):
        return self.__db_id

    @db_id.setter
    def db_id(self, id_str):
        """!WARNING!! -- You probably should not be calling this
                unless you have a very good reason for it"""
        self.__db_id = id_str

if __name__ == '__main__':
    sa = Specialmission()
    print('description is:', sa.description)
    sa.description = 'this is the new description'
    print('new description is:', sa.description)
    sa = None
    print('wiped sa:', sa)
    sa_config = {'description': 'this is description by config',
                 'services': ['Army', 'Scouts']}
    sa = Specialmission(sa_config)
    print('this is sa by config:')
    print('description:', sa.description)
    print('services:', sa.services)
    print('survival roll:', sa.survival_roll)
    sa.survival_roll = 5
    print('new survival roll:', sa.survival_roll)
    sa.title = 'cool special assignment title'
    print('title:', sa.title)
    sa.reward_package = {'cash': 10000,
                         'skills': [['Deception', 0],['Charm', 0]],
                         'items': [['speed shuttle', 1], ['Virus needle gun', 1]],
                         'attributes': [['intelligence', 2]],
                         'promotion': 1,
                         'decorations': ['discretional medal of impunity','silver bong star']}

    print('rewards:', sa.reward_package)
    sa.failure_cost =  {'cash': -500,
                         'attributes': [['intelligence', -1]],
                         'decorations': ['cited for poor impulse control']}
    print('failure cost:', sa.failure_cost)
    sa.mission_requirements = {'attributes' : {'intelligence': 5},
                               'terms':        3,
                               'skills': {'Brawling': 0, 'Pilot': 0}}
    print('mission_requirements:', sa.mission_requirements)
