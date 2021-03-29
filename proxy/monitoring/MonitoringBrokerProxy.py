import time
import psutil
import requests

from util.Logger import Logger
from proxy.logging.LoggingFiwareOrionProxy import LoggingFiwareOrionProxy

class MonitoringBrokerProxy(object):
    def __init__(self, brokerProxy):
        self.__brokerProxy = brokerProxy


    def over(self, protocol):
        self.__brokerProxy.over( protocol )

    
    def connect(self, host, port, keepAlive, onConnect=None):
        self.__brokerProxy.connect( host, port, keepAlive, onConnect )


    def publish(self, topic, payload):
        self.__brokerProxy.publish( topic, payload )

    
    def subscribe(self, topic, onMessage):
        self.__brokerProxy.subscribe( topic, onMessage )

    
    def consume(self):
        self.__brokerProxy.consume()