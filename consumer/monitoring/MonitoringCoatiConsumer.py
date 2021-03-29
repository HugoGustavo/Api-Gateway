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
from consumer.logging.LoggingCoatiConsumer import LoggingCoatiConsumer
from model.dao.ConfigurationDAO import ConfigurationDAO

class MonitoringCoatiConsumer(object):
    def __init__(self, coatiConsumer):
        self.__coatiConsumer = coatiConsumer


    def onConnect(self, message):
        self.__coatiConsumer.onConnect( message )


    def onMessage(self, message):
        self.__coatiConsumer.onMessage( message )

        
    def consume(self):
        properties = ConfigurationDAO( 'Coati' )
        address = StringUtil.clean( properties.get('address.broker') )
        port = StringUtil.toInt( properties.get('port.broker') )
        keepAlive = StringUtil.toInt( properties.get('keep.alive.broker') )
        topic = StringUtil.clean( properties.get('topic.subscribe.broker') )

        self.__brokerProxy = BrokerProxy()
        self.__brokerProxy = LoggingBrokerProxy( self.__brokerProxy )
        self.__brokerProxy = MonitoringBrokerProxy( self.__brokerProxy )
        self.__brokerProxy = ExceptionHandlingBrokerProxy( self.__brokerProxy )

        self.__brokerProxy.over( Protocol.COAP )
        self.__brokerProxy.connect( address, port, keepAlive, self.onConnect )