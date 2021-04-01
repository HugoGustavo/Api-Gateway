import time

from util.Logger import Logger
from util.Monitor import Metric
from util.Monitor import Monitor
from util.Monitor import MetricType
from util.StringUtil import StringUtil
from util.ObjectUtil import ObjectUtil
from model.dao.ConfigurationDAO import ConfigurationDAO
from proxy.monitoring.MonitoringBrokerProxy import MonitoringBrokerProxy

class ExceptionHandlingBrokerProxy(object):
    def __init__(self, brokerProxy):
        self.__brokerProxy = brokerProxy

    
    def over(self, protocol):
        result = None
        try:
            result = self.__brokerProxy.over( protocol )
        
        except Exception as exception:
            classpath = 'proxy.BrokerProxy.over'
            parameters = StringUtil.clean({ 'protocol' : StringUtil.clean( protocol ) })
            exceptionMessage = StringUtil.clean( exception )
            messageError = classpath + '  ' + parameters  + '  ' + exceptionMessage
            Logger.error( messageError )

        return result
    
    
    def connect(self, host, port, keepAlive, onConnect=None):
        result = None
        try:
            result = self.__brokerProxy.connect( host, port, keepAlive, onConnect )
        
        except Exception as exception:
            classpath = 'proxy.BrokerProxy.connect'
            parameters = StringUtil.clean({ 'host' : StringUtil.clean( host ), 'port' : StringUtil.clean( port ), 'keepAlive' : StringUtil.clean( keepAlive ), 'onConnect' : StringUtil.clean( onConnect ) })
            exceptionMessage = StringUtil.clean( exception )
            messageError = classpath + '  ' + parameters  + '  ' + exceptionMessage
            Logger.error( messageError )
        
        return result

    
    def publish(self, topic, payload):
        result = None
        try:
            result = self.__brokerProxy.publish( topic, payload )
        
        except Exception as exception:
            classpath = 'proxy.BrokerProxy.publish'
            parameters = StringUtil.clean({ 'topic' : StringUtil.clean( topic ), 'payload' : StringUtil.clean( payload ) })
            exceptionMessage = StringUtil.clean( exception )
            messageError = classpath + '  ' + parameters  + '  ' + exceptionMessage
            Logger.error( messageError )
        
        return result

    
    def subscribe(self, topic, onMessage):
        result = None
        try:
            result = self.__brokerProxy.subscribe( topic, onMessage )
        
        except Exception as exception:
            classpath = 'proxy.BrokerProxy.subscribe'
            parameters = StringUtil.clean({ 'topic' : StringUtil.clean( topic ), 'onMessage' : StringUtil.clean( onMessage ) })
            exceptionMessage = StringUtil.clean( exception )
            messageError = classpath + '  ' + parameters  + '  ' + exceptionMessage
            Logger.error( messageError )
        
        return result


    def consume(self):
        result = None
        try:
            result = self.__brokerProxy.consume()
        
        except Exception as exception:
            classpath = 'proxy.BrokerProxy.consume'
            parameters = StringUtil.getNoneAsEmpty( None )
            exceptionMessage = StringUtil.clean( exception )
            messageError = classpath + '  ' + parameters  + '  ' + exceptionMessage
            Logger.error( messageError )
        
        return result

