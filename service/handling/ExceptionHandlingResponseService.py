from util.Logger import Logger
from util.Monitor import Metric
from util.Monitor import Monitor
from model.Request import Request
from util.JsonUtil import JsonUtil
from util.Monitor import MetricType
from model.Response import Response
from util.StringUtil import StringUtil
from service.RequestService import RequestService

class ExceptionHandlingResponseService(object):
    def __init__(self, responseService):
        self.__responseService = responseService

    
    def route(self, response):
        result = None
        try:
            result = self.__responseService.route( response )
        
        except Exception as exception:
            classpath = 'service.ResponseService.route'
            parameters = StringUtil.clean({ 'response' : StringUtil.clean( response ) })
            exceptionMessage = StringUtil.clean( exception )
            message = classpath + '  ' + parameters + '  ' + exceptionMessage
            Logger.error( message )

            metric = Monitor.getInstance().findByName( 'app_response_failure_total' )
            metric = Metric() if metric == None else metric
            metric.setName( 'app_response_failure_total' )
            metric.setDescription( 'Total API response failed' )
            metric.setType( MetricType.COUNTER )
            metric.setLabels( None )
            metric.setValue( metric.getValue() + 1)
            Monitor.getInstance().save( metric )
    
        return result
