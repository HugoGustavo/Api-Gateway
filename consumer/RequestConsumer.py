import json
import threading
import paho.mqtt.client as mqtt

from util.Logger import Logger
from model.Request import Request
from service.RequestService import RequestService
from model.dao.ConfigurationDAO import ConfigurationDAO

class RequestConsumer(object):
    def __init__(self):
        self.__properties = ConfigurationDAO('ApiGatewayRequest')
        self.__requestService = RequestService()
        

    def __onConnect(self, client, userdata, flags, rc):
        Logger.info('Connected to Request broker. Client     : ' + str(client))
        Logger.info('Connected to Request broker. User data  : ' + str(userdata))
        Logger.info('Connected to Request broker. Flags      : ' + str(flags))
        Logger.info('Connected to Request broker. Connection : ' + str(rc))

    def __onMessage(self, client, userdata, message):
        Logger.info('Received request. Client   : ' + str(client))
        Logger.info('Received request. User data: ' + str(userdata))
        Logger.info('Received request. Message  : ' + str(message))

        request = Request()
        request_json = json.loads(message.payload)
        request.setReplyHost(str(request_json['replyHost']).strip())
        request.setReplyPort(int(request_json['replyPort']))
        request.setReplyChannel(str(request_json['replyChannel']).strip())
        request.setMethod(str(request_json['method']).strip())
        request.setUri(str(request_json['uri']).strip())
        request.setHeader(str(request_json['header']).strip())
        request.setBody(str(request_json['body']).strip())

        self.__requestService.route(request)
                
    def __onConsume(self):
        try:
            Logger.info("Initializing MQTT Request ...")
            self.__client = mqtt.Client()
            self.__client.on_connect = self.__onConnect
            self.__client.on_message = self.__onMessage

            broker = self.__properties.get('address.broker')
            port = int(self.__properties.get('port.broker'))
            keepAliveBroker = int(self.__properties.get('keep.alive.broker'))
            subscribe = self.__properties.get('topic.subscribe.broker')

            self.__client.connect(broker, port, keepAliveBroker)
            self.__client.subscribe(subscribe)
            self.__client.loop_forever()
        except Exception as exception:
            Logger.error("MQTT Request failed. Cause: " + str(exception))

    def consume(self):
        thread = threading.Thread(target = self.__onConsume)
        thread.start()           