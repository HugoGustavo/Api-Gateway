import json
import threading
import paho.mqtt.client as mqtt

from util.Logger import Logger
from model.Response import Response
from service.ResponseService import ResponseService
from model.dao.ConfigurationDAO import ConfigurationDAO

class ResponseConsumer(object):
    def __init__(self):
        self.__properties = ConfigurationDAO('ApiGatewayResponse')
        self.__responseService = ResponseService ()

    def __onConnect(self, client, userdata, flags, rc):
        Logger.info('Connected to Response broker. Client    : ' + str(client))
        Logger.info('Connected to Response broker. User data : ' + str(userdata))
        Logger.info('Connected to Response broker. Flags     : ' + str(flags))
        Logger.info('Connected to Response broker. Connection: ' + str(rc))

    def __onMessage(self, client, userdata, message):
        Logger.info('Received response. Client   : ' + str(client))
        Logger.info('Received response. User data: ' + str(userdata))
        Logger.info('Received response. Message  : ' + str(message))

        response = Response()
        response_json = json.loads(message.payload)
        response.setId(response_json['id'])
        response.setReplyHost(str(response_json['replyHost']).strip())
        response.setReplyPort(int(response_json['replyPort']))
        response.setReplyChannel(str(response_json['replyChannel']).strip())
        response.setVersionProtocol(str(response_json['versionProtocol']).strip())
        response.setStatusCode(response_json['statusCode'])
        response.setStatusMessage(str(response_json['statusMessage']).strip())
        response.setHeader(str(response_json['header']).strip())
        response.setBody(str(response_json['body']).strip())

        self.__responseService.route(response)

    def __onConsume(self):
        try:
            Logger.info("Initializing MQTT Response ...")
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
            Logger.error("MQTT Response failed. Cause: " + str(exception))

    def consume(self):
        thread = threading.Thread(target = self.__onConsume)
        thread.start()