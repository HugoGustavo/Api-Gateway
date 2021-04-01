import re
import sqlite3

from util.Logger import Logger
from util.Monitor import Metric
from util.Monitor import Monitor
from model.Request import Request
from util.JsonUtil import JsonUtil
from util.Monitor import MetricType
from util.StringUtil import StringUtil
from util.ObjectUtil import ObjectUtil
from model.dao.ConfigurationDAO import ConfigurationDAO
from service.FiwareOrionService import FiwareOrionService
from repository.RequestRepository import RequestRepository

class ExceptionHandlingRequestService(object):
    def __init__(self, requestService):
        self.__requestService = requestService
        
    
    def save(self, request):
        result = None
        try:
            result = self.__requestService.save( request )
        
        except Exception as exception:
            classpath = 'service.RequestService.save'
            parameters = StringUtil.clean({ 'request' : StringUtil.clean( request ) })
            exceptionMessage = StringUtil.clean( exception )
            messageError = classpath + '  ' + parameters + '  ' + exceptionMessage
            Logger.error( messageError )

            metric = Monitor.getInstance().findByName( 'app_request_failure_total' )
            metric = Metric() if metric == None else metric
            metric.setName( 'app_request_failure_total' )
            metric.setDescription( 'Total API request failed' )
            metric.setType( MetricType.COUNTER )
            protocol = StringUtil.clean( request.getOverProtocol().name ).upper()
            labels = ObjectUtil.getDefaultIfEmpty( metric.getLabels(), [ ( 'protocol', protocol ) ] )
            metric.setLabels( labels )
            metric.setValue( metric.getValue() + 1 )
            Monitor.getInstance().save( metric )
        
        return result
    
    
    def findById(self, id):
        result = None
        try:
            result = self.__requestService.findById( id )
        
        except Exception as exception:
            classpath = 'service.RequestService.findById'
            parameters = StringUtil.clean({ 'id' : StringUtil.clean( id ) })
            exceptionMessage = StringUtil.clean( exception )
            message = classpath + '  ' + parameters + '  ' + exceptionMessage
            Logger.error( message )
       
        return result


    
    def route(self, request):
        result = None
        try:
            result = self.__requestService.route( request )
        
        except Exception as exception:
            classpath = 'service.RequestService.route'
            parameters = StringUtil.clean({ 'request' : StringUtil.clean( request ) })
            exceptionMessage = StringUtil.clean( exception )
            message = classpath + '  ' + parameters + '  ' + exceptionMessage
            Logger.error( message )

            metric = Monitor.getInstance().findByName( 'app_request_failure_total' )
            metric = Metric() if metric == None else metric
            metric.setName( 'app_request_failure_total' )
            metric.setDescription( 'Total API request failed' )
            metric.setType( MetricType.COUNTER )
            protocol = StringUtil.clean( request.getOverProtocol().name ).upper()
            labels = ObjectUtil.getDefaultIfEmpty( metric.getLabels(), [ ( 'protocol', protocol ) ] )
            metric.setLabels( labels )
            metric.setValue( metric.getValue() + 1 )
            Monitor.getInstance().save( metric )
        
        return result

