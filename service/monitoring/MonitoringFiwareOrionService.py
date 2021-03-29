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
        self.__fiwareOrionService.read(request)


    def create(self, request):
        self.__fiwareOrionService.create(request)

    
    def update(self, request):
        self.__fiwareOrionService.update(request)


    def delete(self, request):
        self.__fiwareOrionService.delete(request)
