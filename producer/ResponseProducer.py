import paho.mqtt.client as mqtt

from util.StringUtil import StringUtil
from model.dao.ConfigurationDAO import ConfigurationDAO

class ResponseProducer(object):
    def __init__(self):
        self.__properties = ConfigurationDAO( 'ApiGatewayResponse' )


    def produce(self, response):
        broker = StringUtil.clean( self.__properties.get('address.broker') )
        topic = StringUtil.clean( self.__properties.get('topic.subscribe.broker') )

        client = mqtt.Client( 'ApiGateway' )
        client.connect( broker )
        client.publish(topic, StringUtil.clean(response))
