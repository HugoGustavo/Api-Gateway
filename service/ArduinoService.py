import json
import copy
import paho.mqtt.client as mqtt

class ArduinoService(object):
    def __init__(self):
        pass
    
    def route(self, response):
        replyHost = str(response.getReplyHost())
        replyPort = response.getReplyPort()
        replyChannel = str(response.getReplyChannel())
        message = self.__buildMessage(response)

        client = mqtt.Client('ApiGateway')
        client.connect(replyHost, replyPort)
        client.publish(replyChannel, message)

    def __buildMessage(self, response):
        message = copy.deepcopy(response).__dict__

        del message['id']
        del message['replyHost']
        del message['replyPort']
        del message['replyChannel']

        return str(message)