#!/usr/bin/python
import abc
from fate import Fate as fate
from util import datamule


class TravellerObjectManager(object):
    __metaclass__ = abc.ABCMeta

    __targ_object = None
    __fate = None
    __object_names_list = None
    __targ_object_dictionary = None

    def __init__(self):
        self.__fate = fate()
        self.__datamule = datamule

    def create(self):
        """creates an object to manage"""
        pass

    def store(self, obj, targ):
        """stores the object into a repo"""
        datamule.push_dict(obj, targ)

    @property
    def fate(self):
        return self.__fate

    @property
    def datamule(self):
        return self.__datamule

    # def targ_object_dictionary(self):
    #     """gets a dictionary of available objects"""
    #     pass
    @abc.abstractproperty
    def targ_object_dictionary(self):
        return

    @targ_object_dictionary.setter
    def targ_object_dictionary(self, dict):
        pass

    @abc.abstractproperty
    def object_names_list(self):
        """get a list of names for all available objects"""
        pass

    @object_names_list.setter
    def object_names_list(self, objs_list):
        self.__object_names_list = objs_list

    def get_targ_object(self):
        return self.__targ_object

    def set_targ_object(self, targ_object):
        self.__targ_object = targ_object

    def get_prop(self, prop):
        """gets the value of a property of the object"""
        pass

    def set_prop(self, prop, value):
        """sets the objects property"""
        pass
