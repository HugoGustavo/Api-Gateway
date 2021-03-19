import os
import configparser

from os.path import dirname, realpath
from util.StringUtil import StringUtil

class ConfigurationDAO(object):
    def __init__(self, section):
        self.__section = section
        self.__properties = {}
        self.__FILE = str(dirname(dirname(dirname(realpath(__file__))))) + '/conf/apigateway.conf'
        self.__FILE = StringUtil.clean(self.__FILE)

    def get(self, key):
        if ( key not in self.__properties ):
            config = configparser.RawConfigParser()
            config.read(self.__FILE)
            self.__properties[key] =  config.get(self.__section, key)
        return self.__properties[key]