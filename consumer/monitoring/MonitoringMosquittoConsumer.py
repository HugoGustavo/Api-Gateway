import json
import threading
import paho.mqtt.client as mqtt

from util.Logger import Logger
from util.Monitor import Metric
from util.Monitor import Monitor
from util.JsonUtil import JsonUtil
from util.Monitor import MetricType
from util.StringUtil import StringUtil
from consumer.logging.LoggingMosquittoConsumer import LoggingMosquittoConsumer
from model.dao.ConfigurationDAO import ConfigurationDAO

class MonitoringMosquittoConsumer(object):
    def __init__(self, mosquittoConsumser):
        self.__properties = ConfigurationDAO( 'MosquittoInformation' )
        self.__mosquittoConsumser = mosquittoConsumser


    def onConnect(self, client, userdata, flags, rc):
        self.__mosquittoConsumser.onConnect(client, userdata, flags, rc)


    def onMessage(self, client, userdata, message):
        self.__mosquittoConsumser.onMessage(client, userdata, message)

    
    def onConsume(self):
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