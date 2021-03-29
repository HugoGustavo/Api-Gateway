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
from consumer.logging.LoggingResponseConsumer import LoggingResponseConsumer
from model.dao.ConfigurationDAO import ConfigurationDAO

class MonitoringResponseConsumer(object):
    def __init__(self, responseConsumer):
        self.__responseConsumer = responseConsumer
        

    def onConnect(self, message):
        self.__responseConsumer.onConnect( message )
    
    
    def onMessage(self, message):
        response_json = StringUtil.toJson( message.getPayload() )
        response_json['arriveTime'] = time.time()
        message.payload = JsonUtil.toString( response_json )

        metric = Monitor.getInstance().findByName( 'app_response_total' )
        metric = Metric() if metric == None else metric
        metric.setName( 'app_response_total' )
        metric.setDescription( 'Total number of API response' )
        metric.setType( MetricType.COUNTER )
        metric.setLabels( None )
        metric.setValue( metric.getValue() + 1 )
        Monitor.getInstance().save( metric )

        metric = Monitor.getInstance().findByName( 'app_response_bytes_total' )
        metric = Metric() if metric == None else metric
        metric.setName( 'app_response_bytes_total' )
        metric.setDescription( 'Total number of bytes in API response' )
        metric.setType( MetricType.COUNTER )
        metric.setLabels( None )
        value = StringUtil.length( message.payload )
        metric.setValue( metric.getValue() + value )
        Monitor.getInstance().save( metric )

        result = self.__responseConsumer.onMessage( message )
        
        metric = Monitor.getInstance().findByName( 'app_response_success_total' )
        metric = Metric() if metric == None else metric
        metric.setName( 'app_response_success_total' )
        metric.setDescription( 'Total API request successfully' )
        metric.setType( MetricType.COUNTER )
        metric.setLabels( None )
        success = response_json['statusCode'] >= 200 and response_json['statusCode'] <= 299
        value = 1.0 if success else 0.0
        metric.setValue( metric.getValue() + value )
        Monitor.getInstance().save( metric )

        metric = Monitor.getInstance().findByName( 'app_response_failure_total' )
        metric = Metric() if metric == None else metric
        metric.setName( 'app_response_failure_total' )
        metric.setDescription( 'Total API request failed' )
        metric.setType( MetricType.COUNTER )
        metric.setLabels( None )
        success = response_json['statusCode'] >= 200 and response_json['statusCode'] <= 299
        value = 1.0 if not success else 0.0
        metric.setValue( metric.getValue() + value )
        Monitor.getInstance().save( metric ) 

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