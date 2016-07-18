#!/usr/bin/python
import os
from util import datamule, data_config
from travellerobjectmanager import TravellerObjectManager


class ServiceObjectManager(object):
    #__service_data_src = 'data/service_branches'
    __db_cfg = data_config.DB_TARGETS();
    __service_data_src = "" #'data/service_branches'
    __service_branch_dict = {}
    __service_branch_names_list = []
    __targ_object_dictionary = {}

    def __init__(self):
        self.__tom = TravellerObjectManager()
        self.__service_data_src = self.__db_cfg.service_branches

    def __load_services(self):
        """
        resets the list
        fetches names of all available branches in service_branches dir"""
        # open service_branches dir
        data_dir = os.listdir(self.__service_data_src)
        # get all files of the correct name pattern
        #resets the list
        self.__service_branch_names_list = []
        for itm in data_dir:
            if(itm.endswith('svc')):
                service_name = itm.split('.')[0]
                self.__service_branch_names_list.append(service_name)
                # load each into service_branches dict
                dict_path = self.__service_data_src + "/" + itm
                sbd = self.__service_branch_dict
                sbd[service_name] = datamule.fetch_dict(dict_path)
        return self.__service_branch_dict

    @property
    def targ_object_dictionary(self):
        if len(self.__targ_object_dictionary) == 0:
            self.__load_services()
            self.__targ_object_dictionary = self.__service_branch_dict
        return self.__targ_object_dictionary

    @targ_object_dictionary.setter
    def targ_object_dictionary(self, dict):
        self.__targ_object_dictionary = dict

    @property
    def object_names_list(self):
        if len(self.__service_branch_names_list) == 0:
            self.__load_services()
        return self.__service_branch_names_list

    @property
    def service_branches(self):
        return self.object_names_list

    #get service_data by branch name
    def service_data(self, service_name):
        return self.__service_branch_dict[service_name]

    def get_service_skills(self, service_name):
        """returns skills available to be learned in the service"""
        service = self.service_data(service_name)
        key_list = ['aquired_skills',
                    'rank_and_service_skills']

        skills = {}

        for key in key_list:
            skills[key] = service[key]

        return skills

    def store(self, data, path):
        self.__tom.store(data, path)


if __name__ == '__main__':
    som = ServiceObjectManager()
    print('target object dictionary', som.targ_object_dictionary)
    print('object names list', som.object_names_list)
    print('branches',som.service_branches)
    for branch in som.service_branches:
        print('service data keys', branch, list(som.service_data(branch)))
        print('service skills keys', branch, list(som.get_service_skills(branch)))