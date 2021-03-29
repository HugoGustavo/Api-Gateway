from util.Logger import Logger
from util.Monitor import Metric
from util.Monitor import Monitor
from model.Request import Request
from util.JsonUtil import JsonUtil
from util.Monitor import MetricType
from util.StringUtil import StringUtil
from service.ResponseService import ResponseService

class MonitoringResponseService(object):
    def __init__(self, responseService):
        self.__responseService = responseService


    def route(self, response):
        result = self.__responseService.route( response )
        
        return result


