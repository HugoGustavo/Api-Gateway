import time

from util.Logger import Logger
from util.Monitor import Metric
from util.Monitor import Monitor
from util.JsonUtil import JsonUtil
from util.Monitor import MetricType
from util.StringUtil import StringUtil
from service.ArduinoService import ArduinoService

class MonitoringArduinoService(object):
    def __init__(self, service):
        self.__service = service


    def route(self, response):
        response.setDepartureTime( time.time() )

        metric = Monitor.getInstance().findByName( 'app_response_processing_seconds_total' )
        metric = Metric() if metric == None else metric
        metric.setName( 'app_response_processing_seconds_total' )
        metric.setDescription( 'Total response processing time' )
        metric.setType( MetricType.COUNTER )
        metric.setLabels( None )
        value = response.getDepartureTime() - response.getArriveTime()
        metric.setValue( metric.getValue() + value )
        Monitor.getInstance().save( metric )

        self.__service.route( response )

