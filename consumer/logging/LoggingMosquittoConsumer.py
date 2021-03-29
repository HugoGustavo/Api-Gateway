import json
import threading
import paho.mqtt.client as mqtt

from util.Logger import Logger
from util.Monitor import Metric
from util.Monitor import Monitor
from util.JsonUtil import JsonUtil
from util.Monitor import MetricType
from util.StringUtil import StringUtil
from model.vo.Protocol import Protocol
from consumer.MosquittoConsumer import MosquittoConsumer
from model.dao.ConfigurationDAO import ConfigurationDAO

from proxy.BrokerProxy import BrokerProxy
from proxy.monitoring.MonitoringBrokerProxy import MonitoringBrokerProxy
from proxy.logging.LoggingBrokerProxy import LoggingBrokerProxy
from proxy.handling.ExceptionHandlingBrokerProxy import ExceptionHandlingBrokerProxy

class LoggingMosquittoConsumer(object):
    def __init__(self, mosquittoConsumser):
        self.__mosquittoConsumser = mosquittoConsumser

    
    def onConnect(self, message):
        classpath = 'consumer.MosquittoConsumer.onConnect'
        parameters = StringUtil.clean({ 'message' : StringUtil.clean( message ) })
        Logger.debug( classpath + '  ' + parameters )

        self.__mosquittoConsumser.onConnect( message )


    def onMessage(self, message):
        classpath = 'consumer.MosquittoConsumer.onMessage'
        parameters = StringUtil.clean({ 'message' : StringUtil.clean( message ) })
        Logger.debug( classpath + '  ' + parameters )

        self.__mosquittoConsumser.onMessage( message )

    
    def consume(self):
        properties = ConfigurationDAO( 'Mosquitto' )
        address = StringUtil.clean( properties.get('address.broker') )
        port = StringUtil.toInt( properties.get('port.broker') )
        keepAlive = StringUtil.toInt( properties.get('keep.alive.broker') )
        topic = StringUtil.clean( properties.get('topic.subscribe.broker') )

        self.__brokerProxy = BrokerProxy()
        self.__brokerProxy = LoggingBrokerProxy( self.__brokerProxy )
        self.__brokerProxy = MonitoringBrokerProxy( self.__brokerProxy )
        self.__brokerProxy = ExceptionHandlingBrokerProxy( self.__brokerProxy )

        self.__brokerProxy.over( Protocol.MQTT )
        self.__brokerProxy.connect( address, port, keepAlive, self.onConnect )
        self.__brokerProxy.subscribe( topic, self.onMessage )
        self.__brokerProxy.consume()