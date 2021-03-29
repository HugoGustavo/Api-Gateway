import copy
import paho.mqtt.client as mqtt

from util.StringUtil import StringUtil

class IoTService(object):
    def __init__(self):
        pass


    def route(self, response):
        replyHost = StringUtil.clean( response.getReplyHost() )
        replyPort = StringUtil.toInt( response.getReplyPort() )
        replyChannel = StringUtil.clean( response.getReplyChannel() )
        replyProtocol = response.getReplyProtocol()
        message = self.__buildMessage( response )
        message = StringUtil.clean( message )

        client = MQTTClient() if replyProtocol == Protocol.MQTT else COAPClient()
        client.connect(replyHost, replyPort)
        client.publish(replyChannel, message)


    def __buildMessage(self, response):
        message = copy.deepcopy( response )
        message = message.__dict__

        del message['id']
        del message['replyHost']
        del message['replyPort']
        del message['replyChannel']
        del message['replyProtocol']
        del message['overProtocol']
        del message['arriveTime']
        del message['departureTime']

        return message