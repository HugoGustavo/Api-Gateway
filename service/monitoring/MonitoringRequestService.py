import re
import sqlite3

from util.Logger import Logger
from util.Monitor import Metric
from util.Monitor import Monitor
from util.JsonUtil import JsonUtil
from util.Monitor import MetricType
from util.StringUtil import StringUtil
from service.RequestService import RequestService

class MonitoringRequestService(object):
    def __init__(self, requestService):
        self.__requestService = requestService


    def save(self, request):
        result = self.__requestService.save( request )
        
        return result


    def findById(self, id):
        result = self.__requestService.findById( id ) 
        
        return result


    def route(self, request):
        result = self.__requestService.route( request )

        return result
    
