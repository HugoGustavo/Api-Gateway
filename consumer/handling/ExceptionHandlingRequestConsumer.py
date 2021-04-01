import json
import threading
import paho.mqtt.client as mqtt

from util.Logger import Logger
from util.Monitor import Metric
from util.Monitor import Monitor
from util.JsonUtil import JsonUtil
from util.Monitor import MetricType
from util.StringUtil import StringUtil
from util.ObjectUtil import ObjectUtil
from model.vo.Protocol import Protocol
from consumer.monitoring.MonitoringRequestConsumer import MonitoringRequestConsumer
from model.dao.ConfigurationDAO import ConfigurationDAO

from proxy.BrokerProxy import BrokerProxy
from proxy.monitoring.MonitoringBrokerProxy import MonitoringBrokerProxy
from proxy.logging.LoggingBrokerProxy import LoggingBrokerProxy
from proxy.handling.ExceptionHandlingBrokerProxy import ExceptionHandlingBrokerProxy

class ExceptionHandlingRequestConsumer(object):
    def __init__(self, requestConsumer):
        self.__requestConsumer = requestConsumer


    def onConnect(self, message):
        result = None

        try:
            result = self.__requestConsumer.onConnect( message )
        
        except Exception as exception:
            classpath = 'consumer.RequestConsumer.onConnect'
            parameters = StringUtil.clean({ 'message' : StringUtil.clean( message ) })
            exceptionMessage = StringUtil.clean( exception )
            messageError = classpath + '  ' + parameters  + '  ' + exceptionMessage
            Logger.error( messageError )

            metric = Monitor.getInstance().findByName( 'app_request_failure_total' )
            metric = Metric() if metric == None else metric
            metric.setName( 'app_request_failure_total' )
            metric.setDescription( 'Total API request failed' )
            metric.setType( MetricType.COUNTER )
            protocol = StringUtil.clean( message.getProtocol() ).upper()
            labels = ObjectUtil.getDefaultIfEmpty( metric.getLabels(), [ ( 'protocol', protocol ) ] )
            metric.setLabels( labels )
            metric.setValue( metric.getValue() + 1 )
            Monitor.getInstance().save( metric )
        
        return result
    

    def onMessage(self, message):
        result = None
        
        try:
            result = self.__requestConsumer.onMessage( message )
        
        except Exception as exception:
            classpath = 'consumer.RequestConsumer.onMessage'
            parameters = StringUtil.clean({ 'message' : StringUtil.clean( message ) })
            exceptionMessage = StringUtil.clean( exception )
            messageError = classpath + '  ' + parameters  + '  ' + exceptionMessage
            Logger.error( messageError )

            metric = Monitor.getInstance().findByName( 'app_request_failure_total' )
            metric = Metric() if metric == None else metric
            metric.setName( 'app_request_failure_total' )
            metric.setDescription( 'Total API request failed' )
            metric.setType( MetricType.COUNTER )
            protocol = StringUtil.clean( message.getProtocol() ).upper()
            labels = ObjectUtil.getDefaultIfEmpty( metric.getLabels(), [ ( 'protocol', protocol ) ] )
            metric.setLabels( labels )
            metric.setValue( metric.getValue() + 1 )
            Monitor.getInstance().save( metric )
        
        return result

    
    def consume(self):
        properties = ConfigurationDAO( 'RequestMQTT' )
        address = StringUtil.clean( properties.get('address.broker') )
        port = StringUtil.toInt( properties.get('port.broker') )
        keepAlive = StringUtil.toInt( properties.get('keep.alive.broker') )
        topic = StringUtil.clean( properties.get('topic.subscribe.broker') )

        self.__brokerProxy = BrokerProxy()
        self.__brokerProxy = LoggingBrokerProxy( self.__brokerProxy )
        self.__brokerProxy = MonitoringBrokerProxy( self.__brokerProxy )
        self.__brokerProxy = ExceptionHandlingBrokerProxy( self.__brokerProxy )

        self.__brokerProxy.over( Protocol.MQTT )
        self.__brokerProxy.connect( address, port, keepAlive )
        self.__brokerProxy.subscribe( topic, self.onMessage )
        self.__brokerProxy.consume()

        properties = ConfigurationDAO( 'RequestCOAP' )
        address = StringUtil.clean( properties.get('address.broker') )
        port = StringUtil.toInt( properties.get('port.broker') )
        keepAlive = StringUtil.toInt( properties.get('keep.alive.broker') )
        topic = StringUtil.clean( properties.get('topic.subscribe.broker') )

        self.__brokerProxy = BrokerProxy()
        self.__brokerProxy = LoggingBrokerProxy( self.__brokerProxy )
        self.__brokerProxy = MonitoringBrokerProxy( self.__brokerProxy )
        self.__brokerProxy = ExceptionHandlingBrokerProxy( self.__brokerProxy )

        self.__brokerProxy.over( Protocol.COAP )
        self.__brokerProxy.connect( address, port, keepAlive )
        self.__brokerProxy.subscribe( topic, self.onMessage )
        self.__brokerProxy.consume()