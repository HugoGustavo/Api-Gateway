import copy
import paho.mqtt.client as mqtt

from util.Logger import Logger
from util.Monitor import Metric
from util.Monitor import Monitor
from util.JsonUtil import JsonUtil
from util.Monitor import MetricType
from util.StringUtil import StringUtil

class ExceptionHandlingArduinoService(object):
    def __init__(self, arduinoService):
        self.__arduinoService = arduinoService


    def route(self, response):
        try:
            self.__arduinoService.route( response )
        
        except Exception as exception:
            classpath = 'service.ArduinoService.route'
            parameters = StringUtil.clean({ 'response' : StringUtil.clean( response ) })
            exceptionMessage = StringUtil.clean( exception )
            message = classpath + '  ' + parameters  + '  ' + exceptionMessage
            Logger.error( message )

            metric = Monitor.getInstance().findByName( 'app_response_failure_total' )
            metric = Metric() if metric == None else metric
            metric.setName( 'app_response_failure_total' )
            metric.setDescription( 'Total API response failed' )
            metric.setType( MetricType.COUNTER )
            metric.setLabels( None )
            metric.setValue( metric.getValue() + 1 )
            Monitor.getInstance().save( metric )

