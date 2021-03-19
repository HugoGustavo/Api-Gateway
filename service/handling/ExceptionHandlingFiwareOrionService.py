import time
import requests

from util.Logger import Logger
from util.Monitor import Metric
from util.Monitor import Monitor
from model.Request import Request
from util.JsonUtil import JsonUtil
from model.Response import Response
from util.Monitor import MetricType
from util.StringUtil import StringUtil
from producer.ResponseProducer import ResponseProducer
from model.dao.ConfigurationDAO import ConfigurationDAO

class ExceptionHandlingFiwareOrionService(object):
    def __init__(self, fiwareOrionService):
        self.__fiwareOrionService = fiwareOrionService

    
    def read(self, request):
        try:
            self.__fiwareOrionService.read( request )
        
        except Exception as exception:
            classpath = 'service.FiwareOrionService.read'
            parameters = StringUtil.clean({ 'request' : StringUtil.clean(request) })
            exceptionMessage = StringUtil.clean(exception)
            message = classpath + '  ' + parameters  + '  ' + exceptionMessage
            Logger.error( message )

            metric = Monitor.getInstance().findByName( 'app_http_get_fiware_orion_failure_total' )
            metric = Metric() if metric == None else metric
            metric.setName( 'app_http_get_fiware_orion_failure_total' )
            metric.setDescription( 'Total number HTTP GET failed' )
            metric.setType( MetricType.COUNTER )
            metric.setLabels( None )
            metric.setValue( metric.getValue() + 1 )
            Monitor.getInstance().save( metric )

    
    def create(self, request):
        try:
            self.__fiwareOrionService.create( request )
        
        except Exception as exception:
            classpath = 'service.FiwareOrionService.create'
            parameters = StringUtil.clean({ 'request' : StringUtil.clean(request) })
            exceptionMessage = StringUtil.clean(exception)
            message = classpath + '  ' + parameters  + '  ' + exceptionMessage
            Logger.error( message )

            metric = Monitor.getInstance().findByName( 'app_http_post_fiware_orion_failure_total' )
            metric = Metric() if metric == None else metric
            metric.setName( 'app_http_post_fiware_orion_failure_total' )
            metric.setDescription( 'Total number HTTP POST failed' )
            metric.setType( MetricType.COUNTER )
            metric.setLabels( None )
            metric.setValue( metric.getValue() + 1 )
            Monitor.getInstance().save( metric )


    def update(self, request):
        try:
            self.__fiwareOrionService.update( request )
        
        except Exception as exception:
            classpath = 'service.FiwareOrionService.update'
            parameters = StringUtil.clean({ 'request' : StringUtil.clean(request) })
            exceptionMessage = StringUtil.clean(exception)
            message = classpath + '  ' + parameters  + '  ' + exceptionMessage
            Logger.error( message )

            metric = Monitor.getInstance().findByName( 'app_http_patch_fiware_orion_failure_total' )
            metric = Metric() if metric == None else metric
            metric.setName( 'app_http_patch_fiware_orion_failure_total' )
            metric.setDescription( 'Total number HTTP PATCH failed' )
            metric.setType( MetricType.COUNTER )
            metric.setLabels( None )
            metric.setValue( metric.getValue() + 1 )
            Monitor.getInstance().save( metric )

    
    def delete(self, request):
        try:
            self.__fiwareOrionService.delete( request )
        
        except Exception as exception:
            classpath = 'service.FiwareOrionService.delete'
            parameters = StringUtil.clean({ 'request' : StringUtil.clean(request) })
            exceptionMessage = StringUtil.clean(exception)
            message = classpath + '  ' + parameters  + '  ' + exceptionMessage
            Logger.error( message )

            metric = Monitor.getInstance().findByName( 'app_http_delete_fiware_orion_failure_total' )
            metric = Metric() if metric == None else metric
            metric.setName( 'app_http_delete_fiware_orion_failure_total' )
            metric.setDescription( 'Total number HTTP DELETE failed' )
            metric.setType( MetricType.COUNTER )
            metric.setLabels( None )
            metric.setValue( metric.getValue() + 1 )
            Monitor.getInstance().save( metric )

