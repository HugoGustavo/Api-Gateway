import copy
import paho.mqtt.client as mqtt

from util.StringUtil import StringUtil

class ArduinoService(object):
    def __init__(self):
        pass


    def route(self, response):
        replyHost = StringUtil.clean( response.getReplyHost() )
        replyPort = StringUtil.toInt( response.getReplyPort() )
        replyChannel = StringUtil.clean( response.getReplyChannel() )
        message = StringUtil.clean( self.__buildMessage(response) )

        client = mqtt.Client( 'ApiGateway' )
        client.connect(replyHost, replyPort)
        client.publish(replyChannel, message)


    def __buildMessage(self, response):
        message = copy.deepcopy( response ).__dict__

        del message['id']
        del message['replyHost']
        del message['replyPort']
        del message['replyChannel']
        del message['arriveTime']
        del message['departureTime']

        return StringUtil.clean( message )