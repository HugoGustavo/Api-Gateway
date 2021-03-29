import threading
import paho.mqtt.client as mqtt

from util.Logger import Logger
from util.Monitor import Metric
from util.Monitor import Monitor
from util.JsonUtil import JsonUtil
from util.Monitor import MetricType
from util.StringUtil import StringUtil
from model.vo.Protocol import Protocol
from consumer.ResponseConsumer import ResponseConsumer
from model.dao.ConfigurationDAO import ConfigurationDAO

from proxy.BrokerProxy import BrokerProxy
from proxy.monitoring.MonitoringBrokerProxy import MonitoringBrokerProxy
from proxy.logging.LoggingBrokerProxy import LoggingBrokerProxy
from proxy.handling.ExceptionHandlingBrokerProxy import ExceptionHandlingBrokerProxy

class LoggingResponseConsumer(object):
    def __init__(self, responseConsumer):
        self.__responseConsumer = responseConsumer


    def onConnect(self, message):
        classpath = 'consumer.ResponseConsumer.onConnect'
        parameters = StringUtil.clean({ 'message' : StringUtil.clean( message ) })
        Logger.debug( classpath + '  ' + parameters )
        result = self.__responseConsumer.onConnect( message )
        
        return result


    def onMessage(self, message):
        classpath = 'consumer.ResponseConsumer.onMessage'
        parameters = StringUtil.clean({ 'message' : StringUtil.clean( message ) })
        Logger.debug( classpath + '  ' + parameters )
        result = self.__responseConsumer.onMessage( message )

        return result

   
    def consume(self):
        properties = ConfigurationDAO( 'ResponseMQTT' )
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
       
        properties = ConfigurationDAO( 'ResponseCOAP' )
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