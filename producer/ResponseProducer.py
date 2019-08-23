import json
import paho.mqtt.client as mqtt

from model.dao.ConfigurationDAO import ConfigurationDAO

class ResponseProducer(object):
    def __init__(self):
        self.__properties = ConfigurationDAO('ApiGatewayResponse')
    
    def produce(self, response):
        broker = self.__properties.get('address.broker')
        topic = self.__properties.get('topic.subscribe.broker')

        client = mqtt.Client('ApiGateway')
        client.connect(broker)
        client.publish(topic, str(response))