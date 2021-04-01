import time
import requests

from util.Logger import Logger
from util.StringUtil import StringUtil
from util.ObjectUtil import ObjectUtil
from model.vo.Protocol import Protocol
from proxy.BrokerProxy import BrokerProxy

class LoggingBrokerProxy(object):
    def __init__(self, brokerProxy):
        self.__brokerProxy = brokerProxy

    
    def over(self, protocol):
        classpath = 'proxy.BrokerProxy.over'
        parameters = StringUtil.clean({ 'protocol' : StringUtil.clean( protocol ) })
        Logger.debug( classpath + '  ' + parameters )
        result =  self.__brokerProxy.over( protocol )

        return result

    
    def connect(self, host, port, keepAlive, onConnect=None):
        classpath = 'proxy.BrokerProxy.connect'
        parameters = StringUtil.clean({ 'host' : StringUtil.clean( host ), 'port' : StringUtil.clean( port ), 'keepAlive' : StringUtil.clean( keepAlive ), 'onConnect' : StringUtil.clean( onConnect ) })
        Logger.debug( classpath + '  ' + parameters )
        result = self.__brokerProxy.connect( host, port, keepAlive, onConnect )
        
        return result


    def publish(self, topic, payload):
        classpath = 'proxy.BrokerProxy.publish'
        parameters = StringUtil.clean({ 'topic' : StringUtil.clean( topic ), 'payload' : StringUtil.clean( payload ) })
        Logger.debug( classpath + '  ' + parameters )
        result = self.__brokerProxy.publish( topic, payload )
        
        return result

    
    def subscribe(self, topic, onMessage):
        classpath = 'proxy.BrokerProxy.subscribe'
        parameters = StringUtil.clean({ 'topic' : StringUtil.clean( topic ), 'onMessage' : StringUtil.clean( onMessage ) })
        Logger.debug( classpath + '  ' + parameters )
        result = self.__brokerProxy.subscribe( topic, onMessage )

        return result

    
    def consume(self):
        classpath = 'proxy.BrokerProxy.consume'
        parameters = StringUtil.getNoneAsEmpty( None )
        Logger.debug( classpath + '  ' + parameters )
        result = self.__brokerProxy.consume()

        return result
