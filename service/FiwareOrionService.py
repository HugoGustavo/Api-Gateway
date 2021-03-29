import time
import requests

from util.Logger import Logger
from model.Request import Request
from model.Response import Response
from util.StringUtil import StringUtil
from producer.ResponseProducer import ResponseProducer
from model.dao.ConfigurationDAO import ConfigurationDAO

class FiwareOrionService(object):
    def __init__(self, fiwareOrionProxy, responseProducer):
        self.__fiwareOrionProxy = fiwareOrionProxy
        self.__responseProducer = responseProducer


    def read(self, request):
        response = self.__fiwareOrionProxy.read( request )
        result = self.__responseProducer.produce( response ) 
        
        return result


    def create(self, request):
        response = self.__fiwareOrionProxy.create( request )
        result = self.__responseProducer.produce( response ) 
        
        return result


    def update(self, request):
        response = self.__fiwareOrionProxy.update( request )
        result = self.__responseProducer.produce( response )

        return result


    def delete(self, request):
        response = self.__fiwareOrionProxy.delete( request )
        result = self.__responseProducer.produce( response )

        return result