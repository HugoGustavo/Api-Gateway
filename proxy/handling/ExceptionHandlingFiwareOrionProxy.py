import time

from util.Logger import Logger
from util.Monitor import Metric
from util.Monitor import Monitor
from model.Request import Request
from util.Monitor import MetricType
from util.StringUtil import StringUtil
from proxy.monitoring.MonitoringFiwareOrionProxy import MonitoringFiwareOrionProxy

class ExceptionHandlingFiwareOrionProxy(object):
    def __init__(self, fiwareOrionProxy):
        self.__fiwareOrionProxy = fiwareOrionProxy

    
    def read(self, request):
        result = None
        try:
            result = self.__fiwareOrionProxy.read( request )
        
        except Exception as exception:
            classpath = 'proxy.FiwareOrionProxy.read'
            parameters = StringUtil.clean({ 'request' : StringUtil.clean( request ) })
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
    
        return result


    
    def create(self, request):
        result = None
        try:
            result = self.__fiwareOrionProxy.create( request )
        
        except Exception as exception:
            classpath = 'proxy.FiwareOrionProxy.create'
            parameters = StringUtil.clean({ 'request' : StringUtil.clean( request ) })
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
        
        return result


    def update(self, request):
        result = None
        try:
            result = self.__fiwareOrionProxy.update( request )
        
        except Exception as exception:
            classpath = 'proxy.FiwareOrionProxy.update'
            parameters = StringUtil.clean({ 'request' : StringUtil.clean( request ) })
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
        
        return result

    
    def delete(self, request):
        result = None
        try:
            result = self.__fiwareOrionProxy.delete( request )
        
        except Exception as exception:
            classpath = 'proxy.FiwareOrionProxy.delete'
            parameters = StringUtil.clean({ 'request' : StringUtil.clean( request ) })
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
        
        return result
