import json
import threading
import paho.mqtt.client as mqtt

from util.Logger import Logger
from model.Request import Request
from util.JsonUtil import JsonUtil
from util.StringUtil import StringUtil
from service.RequestService import RequestService
from model.dao.ConfigurationDAO import ConfigurationDAO
from service.monitoring.MonitoringRequestService import MonitoringRequestService

class RequestConsumer(object):
    def __init__(self, requestService):
        self.__properties = ConfigurationDAO( 'ApiGatewayRequest' )
        self.__requestService = requestService


    def onConnect(self, client, userdata, flags, rc):
        pass


    def onMessage(self, client, userdata, message):
        request = Request()
        request_json = StringUtil.toJson(message.payload)
        request.setReplyHost( StringUtil.clean(request_json['replyHost']) )
        request.setReplyPort( StringUtil.toInt(request_json['replyPort']) )
        request.setReplyChannel( StringUtil.clean(request_json['replyChannel']) )
        request.setMethod( StringUtil.clean(request_json['method']) )
        request.setUri( StringUtil.clean(request_json['uri']) )
        request.setHeader( StringUtil.clean(request_json['header']) )
        request.setBody( StringUtil.clean(request_json['body']) )
        request.setArriveTime( StringUtil.toFloat(request_json.get('arriveTime', None)) )
        request.setDepartureTime( None )

        self.__requestService.route(request)


    def onConsume(self):
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
    
    
    def consume(self):
        thread = threading.Thread(target = self.onConsume)
        thread.start() 