from util.Logger import Logger
from util.Monitor import Metric
from util.Monitor import Monitor
from util.JsonUtil import JsonUtil
from util.Monitor import MetricType
from util.StringUtil import StringUtil
from service.ResponseService import ResponseService

class LoggingResponseService(object):
    def __init__(self, service):
        self.__responseService = service


    def route(self, response):
        classpath = 'service.ResponseService.route'
        parameters = StringUtil.clean({ 'response' : StringUtil.clean( response ) })
        Logger.debug( classpath + '  ' + parameters )
        result = self.__responseService.route( response )

        return result


