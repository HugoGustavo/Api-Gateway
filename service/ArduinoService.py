import json
import copy
import time
import socket
import threading
import paho.mqtt.client as mqtt

from model.dao.ConfigurationDAO import ConfigurationDAO
from producer.RequestProducer import RequestProducer

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
        
    def consume(self):
        thread = threading.Thread(target = self.__consume)
        thread.start()

    def __consume(self):
        requestProducer = RequestProducer()
        properties = ConfigurationDAO('Arduino')
        address = str(properties.get('address'))
        port = int(properties.get('port'))
        while True:
            try: 
                s = socket.socket()
                s.connect((address, port))
                s.send(b'GET')
                message = str(s.recv(1024), 'utf-8')
                print(message)
                s.close()
                requestProducer.produce(message)
                time.sleep(5)
            except Exception as e:
                print(str(e))
            
            
        