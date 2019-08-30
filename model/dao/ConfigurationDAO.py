import os
import configparser

os.path.abspath(os.path.join('conf/conf', os.pardir))
class ConfigurationDAO(object):
    def __init__(self, section):
        self.__section = section
        self.__properties = {}
        self.__FILE = os.path.abspath(os.path.join('conf/conf', os.pardir)) + '/apigateway.conf'

    def get(self, key):
        if ( key not in self.__properties ):
            config = configparser.RawConfigParser()
            config.read(self.__FILE)
            self.__properties[key] =  config.get(self.__section, key)
        return self.__properties[key]