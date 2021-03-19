import json
import threading
import paho.mqtt.client as mqtt

from util.Logger import Logger
from model.Response import Response
from util.StringUtil import StringUtil
from service.ResponseService import ResponseService
from model.dao.ConfigurationDAO import ConfigurationDAO

class ResponseConsumer(object):
    def __init__(self, responseService):
        self.__properties = ConfigurationDAO( 'ApiGatewayResponse' )
        self.__responseService = responseService


    def onConnect(self, client, userdata, flags, rc):
        pass


    def onMessage(self, client, userdata, message):
        response = Response()
        response_json = StringUtil.toJson(message.payload)
        response.setId( response_json['id'] )
        response.setReplyHost( StringUtil.clean(response_json['replyHost']) )
        response.setReplyPort( StringUtil.toInt(response_json['replyPort']) )
        response.setReplyChannel( StringUtil.clean(response_json['replyChannel']) )
        response.setVersionProtocol( StringUtil.clean(response_json['versionProtocol']) )
        response.setStatusCode( response_json['statusCode'] )
        response.setStatusMessage( StringUtil.clean(response_json['statusMessage']) )
        response.setHeader( StringUtil.clean(response_json['header']) )
        response.setBody( StringUtil.clean(response_json['body']) )
        response.setArriveTime( StringUtil.toFloat(response_json.get('arriveTime', None)) )
        response.setDepartureTime( None )

        self.__responseService.route(response)


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
            parameters = StringUtil.clean({ })
            exceptionMessage = StringUtil.clean(exception)
            message = classpath + '  ' + parameters  + '  ' + exceptionMessage
            Logger.error( message )
        

    def consume(self):
        thread = threading.Thread(target = self.onConsume)
        thread.start()