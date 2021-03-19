import threading
import paho.mqtt.client as mqtt

from util.Logger import Logger
from util.Monitor import Metric
from util.Monitor import Monitor
from util.JsonUtil import JsonUtil
from util.Monitor import MetricType
from util.StringUtil import StringUtil
from consumer.RequestConsumer import RequestConsumer
from model.dao.ConfigurationDAO import ConfigurationDAO

class LoggingRequestConsumer(object):
    def __init__(self, requestConsumer):
        self.__properties = ConfigurationDAO( 'ApiGatewayRequest' )
        self.__requestConsumer = requestConsumer

    
    def onConnect(self, client, userdata, flags, rc):
        classpath = 'consumer.RequestConsumer.onConnect'
        parameters = StringUtil.clean({ 'client' : StringUtil.clean( client ), 'userdata' : StringUtil.clean( userdata ), 'flags' : StringUtil.clean( flags ), 'rc' : StringUtil.clean( rc ) })
        Logger.debug( classpath + '  ' + parameters )
        self.__requestConsumer.onConnect(client, userdata, flags, rc)
        
    
    def onMessage(self, client, userdata, message):
        classpath = 'consumer.RequestConsumer.onMessage'
        parameters = StringUtil.clean({ 'client' : StringUtil.clean( client ), 'userdata' : StringUtil.clean( userdata ), 'message' : StringUtil.clean( message.payload ) })
        Logger.debug( classpath + '  ' + parameters )
        self.__requestConsumer.onMessage(client, userdata, message)

    def onConsume(self):
        classpath = 'consumer.RequestConsumser.onConnect'
        parameters = StringUtil.getNoneAsEmpty(None)
        Logger.debug( classpath + '  ' + parameters )

        try:
            Logger.info("Initializing MQTT Request ...")
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
            classpath = 'consumer.RequestConsumer.onConsume'
            parameters = StringUtil.getNoneAsEmpty( None )
            exceptionMessage = StringUtil.clean( exception )
            message = classpath + '  ' + parameters  + '  ' + exceptionMessage
            Logger.error( message )
    
            metric = Monitor.getInstance().findByName( 'app_request_failure_total' )
            metric = Metric() if metric == None else metric
            metric.setName( 'app_request_failure_total' )
            metric.setDescription( 'Total API request failed' )
            metric.setType( MetricType.COUNTER )
            metric.setLabels( None )
            metric.setValue( metric.getValue() + 1 )
            Monitor.getInstance().save( metric )
    
    def consume(self):
        thread = threading.Thread(target = self.onConsume)
        thread.start()
