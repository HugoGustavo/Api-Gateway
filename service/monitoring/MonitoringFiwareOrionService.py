import time
import psutil
import requests

from util.Logger import Logger
from util.Monitor import Metric
from util.Monitor import Monitor
from model.Request import Request
from util.JsonUtil import JsonUtil
from util.Monitor import MetricType
from util.StringUtil import StringUtil
from service.FiwareOrionService import FiwareOrionService

class MonitoringFiwareOrionService(object):
    def __init__(self, fiwareOrionService):
        self.__fiwareOrionService = fiwareOrionService


    def read(self, request):
        result = self.__fiwareOrionService.read( request )

        return result


    def create(self, request):
        result = self.__fiwareOrionService.create( request )

        return result

    
    def update(self, request):
        result = self.__fiwareOrionService.update( request )

        return result


    def delete(self, request):
        result = self.__fiwareOrionService.delete( request )
        
        return result
