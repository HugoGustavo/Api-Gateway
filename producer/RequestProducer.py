import json
import paho.mqtt.client as mqtt

from model.dao.ConfigurationDAO import ConfigurationDAO

class RequestProducer(object):
    def __init__(self):
        self.__properties = ConfigurationDAO('ApiGatewayRequest')
    
    def produce(self, request):
        broker = self.__properties.get('address.broker')
        topic = self.__properties.get('topic.subscribe.broker')

        client = mqtt.Client('ApiGateway')
        client.connect(broker)
        client.publish(topic, str(request))