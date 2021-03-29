import time
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
from consumer.logging.LoggingRequestConsumer import LoggingRequestConsumer
from model.dao.ConfigurationDAO import ConfigurationDAO

class MonitoringRequestConsumer(object):
    def __init__(self, requestConsumer):
        self.__requestConsumer = requestConsumer


    def onConnect(self, message):
        self.__requestConsumer.onConnect( message )    

    
    def onMessage(self, message):
        request_json = StringUtil.toJson( message.getPayload() )
        request_json['arriveTime'] = time.time()
        message.payload = JsonUtil.toString( request_json )

        metric = Monitor.getInstance().findByName( 'app_request_total' )
        metric = Metric() if metric == None else metric
        metric.setName( 'app_request_total' )
        metric.setDescription( 'Total number of API request' )
        metric.setType( MetricType.COUNTER )
        metric.setLabels( None )
        metric.setValue( metric.getValue() + 1 )
        Monitor.getInstance().save( metric )

        metric = Monitor.getInstance().findByName( 'app_request_bytes_total' )
        metric = Metric() if metric == None else metric
        metric.setName( 'app_request_bytes_total' )
        metric.setDescription( 'Total number of bytes in API request' )
        metric.setType( MetricType.COUNTER )
        metric.setLabels( None )
        value = StringUtil.length( message.getPayload() )
        metric.setValue( metric.getValue() + value )
        Monitor.getInstance().save( metric )
        
        self.__requestConsumer.onMessage( message )

        metric = Monitor.getInstance().findByName( 'app_request_success_total' )
        metric = Metric() if metric == None else metric
        metric.setName( 'app_request_success_total' )
        metric.setDescription( 'Total API request successfully' )
        metric.setType( MetricType.COUNTER )
        metric.setLabels( None )
        metric.setValue( metric.getValue() + 1 )
        Monitor.getInstance().save( metric )


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
