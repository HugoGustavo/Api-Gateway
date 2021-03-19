from util.Logger import Logger
from util.Monitor import Metric
from util.Monitor import Monitor
from util.JsonUtil import JsonUtil
from util.Monitor import MetricType
from util.StringUtil import StringUtil
from service.ArduinoService import ArduinoService

class LoggingArduinoService(object):
    def __init__(self, service):
        self.__service = service


    def route(self, response):
        classpath = 'service.ArduinoService.route'
        parameters = StringUtil.clean({ 'response' : StringUtil.clean( response ) })
        Logger.debug( classpath + '  ' + parameters )
        self.__service.route( response )

