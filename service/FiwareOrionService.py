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
        self.__responseProducer.produce( response ) 


    def create(self, request):
        response = self.__fiwareOrionProxy.create( request )
        self.__responseProducer.produce( response ) 


    def update(self, request):
        response = self.__fiwareOrionProxy.update( request )
        self.__responseProducer.produce( response ) 


    def delete(self, request):
        response = self.__fiwareOrionProxy.delete( request )
        self.__responseProducer.produce( response ) 