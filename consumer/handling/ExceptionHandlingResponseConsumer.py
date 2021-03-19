import json
import threading
import paho.mqtt.client as mqtt

from util.Logger import Logger
from util.Monitor import Metric
from util.Monitor import Monitor
from util.JsonUtil import JsonUtil
from util.Monitor import MetricType
from util.StringUtil import StringUtil
from consumer.monitoring.MonitoringResponseConsumer import MonitoringResponseConsumer
from model.dao.ConfigurationDAO import ConfigurationDAO

class ExceptionHandlingResponseConsumer(object):
    def __init__(self, responseConsumer):
        self.__properties = ConfigurationDAO( 'ApiGatewayResponse' )
        self.__responseConsumer = responseConsumer


    def onConnect(self, client, userdata, flags, rc):
        try:
            self.__responseConsumer.onConnect(client, userdata, flags, rc)
        
        except Exception as exception:
            classpath = 'consumer.responseConsumer.onConnect'
            parameters = StringUtil.clean({ 'client' : StringUtil.clean( client ), 'userdata' : StringUtil.clean( userdata ), 'flags' : StringUtil.clean( flags ), 'rc' : StringUtil.clean( rc ) })
            exceptionMessage = StringUtil.clean( exception )
            message = classpath + '  ' + parameters  + '  ' + exceptionMessage
            Logger.error( message )

            metric = Monitor.getInstance().findByName( 'app_response_failure_total' )
            metric = Metric() if metric == None else metric
            metric.setName( 'app_response_failure_total' )
            metric.setDescription( 'Total API response failed' )
            metric.setType( MetricType.COUNTER )
            metric.setLabels( None )
            metric.setValue( metric.getValue() + 1 )
            Monitor.getInstance().save(metric)

    
    def onMessage(self, client, userdata, message):
        try:
            self.__responseConsumer.onMessage(client, userdata, message)
        
        except Exception as exception:
            classpath = 'consumer.responseConsumer.onMessage'
            parameters = StringUtil.clean({ 'client' : StringUtil.clean( client ), 'userdata' : StringUtil.clean( userdata ), 'message' : StringUtil.clean( message ) })
            exceptionMessage = StringUtil.clean( exception )
            message = classpath + '  ' + parameters  + '  ' + exceptionMessage
            Logger.error( message )

            metric = Monitor.getInstance().findByName( 'app_response_failure_total' )
            metric = Metric() if metric == None else metric
            metric.setName( 'app_response_failure_total' )
            metric.setDescription( 'Total API response failed' )
            metric.setType( MetricType.COUNTER )
            metric.setLabels( None )
            metric.setValue( metric.getValue() + 1 )
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
            metric.setLabels( None )
            metric.setValue( metric.getValue() + 1 )
            Monitor.getInstance().save( metric )
        

    def consume(self):
        thread = threading.Thread(target = self.onConsume)
        thread.start()