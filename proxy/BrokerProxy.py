import threading

from util.ObjectUtil import ObjectUtil
from util.StringUtil import StringUtil
from util.BrokerClient import MQTTClient
from util.BrokerClient import COAPClient
from model.vo.Protocol import Protocol

class BrokerProxy(object):
    def __init__(self, id=None, protocol=None):
        self.__id = id
        self.__protocol = protocol

    
    def over(self, protocol):
        self.__protocol = protocol
    
    
    def connect(self, host, port, keepAlive, onConnect=None):
        self.__id = StringUtil.getNoneAsEmpty( self.__id )
        self.__id = StringUtil.clean( self.__id )
        host = ObjectUtil.getDefaultIfNone( host, "127.0.0.1" )
        host = StringUtil.clean( host )
        port = ObjectUtil.getDefaultIfNone( port, 1883 )
        port = StringUtil.clean( port )
        port = StringUtil.toInt( port )
        keepAlive = ObjectUtil.getDefaultIfNone( keepAlive, 60 )
        keepAlive = StringUtil.clean( keepAlive )
        keepAlive = StringUtil.toInt( keepAlive )

        self.__client = MQTTClient( self.__id ) if self.__protocol == Protocol.MQTT else COAPClient( self.__id )
        self.__client.setOnConnect( onConnect )
        result = self.__client.connect( host, port, keepAlive )

        return result
    
    
    def publish(self, topic, payload):
        if( self.__client == None ): return

        topic = StringUtil.getNoneAsEmpty( topic )
        topic = StringUtil.clean( topic )
        payload = StringUtil.getNoneAsEmpty( payload )
        
        result = self.__client.publish( topic, payload )

        return result

    
    def subscribe(self, topic, onMessage):
        if ( self.__client == None ): return
        
        topic = StringUtil.getNoneAsEmpty( topic )
        topic = StringUtil.clean( topic )

        self.__client.setOnMessage( onMessage )
        result = self.__client.subscribe( topic )
    
        return result
    
    
    def consume(self):
        if ( self.__client == None ): return

        result = self.__client.consume()

        return result