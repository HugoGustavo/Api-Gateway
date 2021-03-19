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
    def __init__(self, service):
        self.__service = service


    def save(self, request):
        result = self.__service.save( request )
        return result


    def findById(self, id):
        result = self.__service.findById( id ) 
        return result


    def route(self, request):
        self.__service.route( request )
    
