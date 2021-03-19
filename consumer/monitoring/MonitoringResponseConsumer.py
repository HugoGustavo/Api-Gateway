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
from consumer.logging.LoggingResponseConsumer import LoggingResponseConsumer
from model.dao.ConfigurationDAO import ConfigurationDAO

class MonitoringResponseConsumer(object):
    def __init__(self, responseConsumer):
        self.__properties = ConfigurationDAO( 'ApiGatewayResponse' )
        self.__responseConsumer = responseConsumer
        

    def onConnect(self, client, userdata, flags, rc):
        self.__responseConsumer.onConnect(client, userdata, flags, rc)


    def onMessage(self, client, userdata, message):
        response_json = StringUtil.toJson(message.payload)
        response_json['arriveTime'] = time.time()
        message.payload = JsonUtil.toString(response_json)

        metric = Monitor.getInstance().findByName( 'app_api_response_total' )
        metric = Metric() if metric == None else metric
        metric.setName( 'app_api_response_total' )
        metric.setDescription( 'Total number of API response' )
        metric.setType( MetricType.COUNTER )
        metric.setLabels( None )
        metric.setValue( metric.getValue() + 1 )
        Monitor.getInstance().save( metric )

        metric = Monitor.getInstance().findByName( 'app_api_response_bytes_total' )
        metric = Metric() if metric == None else metric
        metric.setName( 'app_api_response_bytes_total' )
        metric.setDescription( 'Total number of bytes in API response' )
        metric.setType( MetricType.COUNTER )
        metric.setLabels( None )
        value = StringUtil.length( message.payload )
        metric.setValue( metric.getValue() + value )
        Monitor.getInstance().save( metric )

        self.__responseConsumer.onMessage(client, userdata, message)
        
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


    def onConsume(self):
        try:
            Logger.info("Initializing MQTT Response ...")
            self.__client = mqtt.Client()
            self.__client.on_connect = self.onConnect
            self.__client.on_message = self.onMessage

            broker = StringUtil.clean( self.__properties.get('address.broker') )
            port = StringUtil.toInt( self.__properties.get('port.broker') )
            keepAliveBroker = StringUtil.toInt( self.__properties.get('keep.alive.broker') )
            subscribe = StringUtil.clean( self.__properties.get('topic.subscribe.broker') )

            self.__client.connect(broker, port, keepAliveBroker)
            self.__client.subscribe( subscribe )
            self.__client.loop_forever()
        
        except Exception as exception:
            classpath = 'consumer.ResponseConsumer.onConsume'
            parameters = StringUtil.getNoneAsEmpty( None )
            exceptionMessage = StringUtil.clean( exception )
            message = classpath + '  ' + parameters  + '  ' + exceptionMessage
            Logger.error( message )

            metric = Monitor.getInstance().findByName( 'app_response_failure_total' )
            metric = Metric() if metric == None else metric
            metric.setName( 'app_response_failure_total' )
            metric.setDescription( 'Total API response failed' )
            metric.setType( MetricType.COUNTER )
            metric.setValue( metric.getValue() + 1 )
            Monitor.getInstance().save( metric )
        

    def consume(self):
        thread = threading.Thread(target = self.onConsume)
        thread.start()