import time
import psutil
import requests

from util.Logger import Logger
from proxy.logging.LoggingFiwareOrionProxy import LoggingFiwareOrionProxy

class MonitoringBrokerProxy(object):
    def __init__(self, brokerProxy):
        self.__brokerProxy = brokerProxy


    def over(self, protocol):
        result = self.__brokerProxy.over( protocol )

        return result

    
    def connect(self, host, port, keepAlive, onConnect=None):
        result = self.__brokerProxy.connect( host, port, keepAlive, onConnect )
        
        return result


    def publish(self, topic, payload):
        result = self.__brokerProxy.publish( topic, payload )

        return result

    
    def subscribe(self, topic, onMessage):
        result = self.__brokerProxy.subscribe( topic, onMessage )

        return result

    
    def consume(self):
        result = self.__brokerProxy.consume()
        
        return result