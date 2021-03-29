from util.Logger import Logger
from util.Monitor import Metric
from util.Monitor import Monitor
from util.JsonUtil import JsonUtil
from util.Monitor import MetricType
from util.StringUtil import StringUtil
from service.IoTService import IoTService

class LoggingIoTService(object):
    def __init__(self, iotService):
        self.__iotService = iotService


    def route(self, response):
        classpath = 'service.IoTService.route'
        parameters = StringUtil.clean({ 'response' : StringUtil.clean( response ) })
        Logger.debug( classpath + '  ' + parameters )
        self.__iotService.route( response )

