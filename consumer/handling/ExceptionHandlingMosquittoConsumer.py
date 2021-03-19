import json
import threading
import paho.mqtt.client as mqtt

from util.Logger import Logger
from util.Monitor import Metric
from util.Monitor import MetricType
from util.Monitor import Monitor
from util.JsonUtil import JsonUtil
from util.StringUtil import StringUtil
from consumer.monitoring.MonitoringMosquittoConsumer import MonitoringMosquittoConsumer
from model.dao.ConfigurationDAO import ConfigurationDAO

class ExceptionHandlingMosquittoConsumer(object):
    def __init__(self, mosquittoConsumser):
        self.__properties = ConfigurationDAO( 'MosquittoInformation' )
        self.__mosquittoConsumser = mosquittoConsumser


    def onConnect(self, client, userdata, flags, rc):
        try:
            self.__mosquittoConsumser.onConnect(client, userdata, flags, rc)
        
        except Exception as exception:
            classpath = 'consumer.MosquittoConsumer.onConnect'
            parameters = StringUtil.clean({ 'client' : StringUtil.clean( client ), 'userdata' : StringUtil.clean( userdata ), 'flags' : StringUtil.clean( flags ), 'rc' : StringUtil.clean( rc ) })
            exceptionMessage = StringUtil.clean( exception )
            message = classpath + '  ' + parameters  + '  ' + exceptionMessage
            Logger.error( message )


    def onMessage(self, client, userdata, message):
        try:
            self.__mosquittoConsumser.onMessage(client, userdata, message)
        
        except Exception as exception:
            classpath = 'consumer.RequestConsumer.onMessage'
            parameters = StringUtil.clean({ 'client' : StringUtil.clean( client ), 'userdata' : StringUtil.clean( userdata ), 'message' : StringUtil.clean( message ) })
            exceptionMessage = StringUtil.clean( exception )
            message = classpath + '  ' + parameters  + '  ' + exceptionMessage
            Logger.error( message )

    
    def onConsume(self):
        classpath = 'consumer.MosquittoConsumer.onConsume'
        parameters = StringUtil.getNoneAsEmpty( None )
        Logger.debug( classpath + '  ' + parameters )
        
        try:
            Logger.info("Initializing MQTT Information ...")
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
            classpath = 'consumer.MosquittoConsumer.onConsume'
            parameters = StringUtil.getNoneAsEmpty( None )
            exceptionMessage = StringUtil.clean( exception )
            message = classpath + '  ' + parameters  + '  ' + exceptionMessage
            Logger.error( message )

    
    def consume(self):
        thread = threading.Thread(target = self.onConsume)
        thread.start() 