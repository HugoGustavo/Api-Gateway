import json
import enum
import time
import threading
import paho.mqtt.client as mqtt

from coapthon import defines
from coapthon.client.helperclient import HelperClient

from util.Logger import Logger
from util.ListUtil import ListUtil
from util.StringUtil import StringUtil
from coapthon.client.helperclient import HelperClient
from model.dao.ConfigurationDAO import ConfigurationDAO

class Message(object):
    def __init__(self, payload=None, topic=None, protocol=None):
        self.payload = payload
        self.topic = topic
        self.protocol = protocol

    
    def getPayload(self):
        return self.payload
    

    def setPayload(self, payload):
        self.payload = payload
    
    
    def getTopic(self):
        return self.topic
    
    
    def setTopic(self, topic):
        self.topic = topic

    
    def getProtocol(self):
        return self.protocol
    
    
    def setProtocol(self, protocol):
        self.protocol = protocol

    
    def __str__(self):
        result = dict()
        result['payload'] = str(self.payload)
        result['topic'] = str(self.topic)
        result['protocol'] = str(self.protocol)
        return str( result )


class MQTTClient(object):
    def __init__(self, id=None):
        self.__client = mqtt.Client(id)
        self.__client.on_connect = self.__wrapperOnConnect
        self.__client.on_message = self.__wrapperOnMessage
        
        self.__onConnect = None
        self.__onMessage = None
    
    
    def connect(self, host, port=1883, keepAlive=60, bindAddress=""):
        result = self.__client.connect(host, port, keepAlive, bindAddress)
        return result

    
    def publish(self, topic, payload=None, qos=0, retain=False):
        result = self.__client.publish(topic, payload, qos, retain)
        return result

   
    def subscribe(self, topic, qos=0):
        result = self.__client.subscribe(topic, qos)
        return result

    
    def loopForever(self, timeout=1.0, maxPackets=1, retryFirstConnection=False):
        self.__client.loop_forever()

    
    def consume(self):
        thread = threading.Thread(target = self.loopForever)
        thread.start()
        
    
    def getOnMessage(self):
        return self.__onMessage
    

    def setOnMessage(self, onMessage):
        self.__onMessage = onMessage
    

    def getOnConnect(self):
        return self.__onConnect

    
    def setOnConnect(self, onConnect):
        self.__onConnect = onConnect

    
    def __wrapperOnConnect(self, client, userdata, flags, rc):
        if( self.__onConnect == None ): return

        message = Message()
        message.setPayload( StringUtil.getNoneAsEmpty(None) )
        message.setTopic( StringUtil.getNoneAsEmpty(None) )
        message.setProtocol( StringUtil.clean('MQTT') )
        
        self.__onConnect( message )

    
    def __wrapperOnMessage(self, client, userdata, message):
        if( self.__onMessage == None ): return
        
        result = Message()
        result.setPayload( message.payload )
        result.setTopic( message.topic )
        result.setProtocol( StringUtil.clean('MQTT') )
        
        self.__onMessage( result )




class COAPClient(object):
    def __init__(self, id=None):
        self.__client = None
        self.__onConnect = None
        self.__onMessage = None
    
 
    def connect(self, host="127.0.0.1", port=5683, keepAlive=60):
        self.__host = StringUtil.getNoneAsEmpty( host )
        self.__host = StringUtil.clean( self.__host )
        self.__port = StringUtil.getNoneAsEmpty( port )
        self.__port = StringUtil.clean( self.__port )
        self.__port = StringUtil.toInt( self.__port )
        self.__keepAlive = StringUtil.clean( keepAlive )
        self.__keepAlive = StringUtil.toInt( self.__keepAlive )
        server = ( self.__host, self.__port )
        self.__client = HelperClient( server=server )
        self.__timestampConnection = time.time()

        result = Message()
        result.setPayload( StringUtil.getNoneAsEmpty(None) )
        result.setTopic( StringUtil.getNoneAsEmpty(None) )
        result.setProtocol( StringUtil.clean('CoAP') )
        
        self.__wrapperOnConnect( result )


    def publish(self, topics=None, message=None):
        if self.__client == None: return None
        

        topics = StringUtil.getNoneAsEmpty( topics )
        topics = StringUtil.replace( topics, "//", "/" )
        topics = StringUtil.clean( topics )
        message = StringUtil.getNoneAsEmpty( message )

        if ( self.__isConnectionExpired() ): self.__reconnect()
        
        response = self.__client.put( topics, message, timeout=self.__keepAlive )

        result = Message()
        result.setPayload( StringUtil.clean(response.payload) )
        result.setTopic( StringUtil.clean(topics) )
        result.setProtocol( StringUtil.clean('CoAP') )
        
        return result

    def subscribe(self, topics=None):
        self.__topics = StringUtil.getNoneAsEmpty( topics )
        self.__topics = StringUtil.replace( self.__topics, "//", "/" )
        self.__topics = StringUtil.clean( self.__topics )
    

    def loopForever(self):        
        response = self.__client.observe( self.__topics, callback=self.__wrapperOnMessage, timeout=self.__keepAlive )
        
        result = Message()
        result.setPayload( StringUtil.clean(response.payload) if response != None else StringUtil.getNoneAsEmpty(None) )
        result.setTopic( StringUtil.clean(self.__topics) )
        result.setProtocol( StringUtil.clean('CoAP') )

        return result

    
    def consume(self):
        if ( StringUtil.isEmpty( self.__topics ) ): return
        
        self.__client.put( self.__topics, StringUtil.getNoneAsEmpty( None ) )
        
        return self.loopForever()
        

    def getOnMessage(self):
        return self.__onMessage
    

    def setOnMessage(self, onMessage):
        self.__onMessage = onMessage
    

    def getOnConnect(self):
        return self.__onConnect

    
    def setOnConnect(self, onConnect):
        self.__onConnect = onConnect


    def __wrapperOnConnect(self, message):
        if( message == None ): return
        if( self.__onConnect == None ): return 

        result = Message()
        result.setPayload( StringUtil.getNoneAsEmpty(None) )
        result.setTopic( StringUtil.getNoneAsEmpty(None) )
        result.setProtocol( StringUtil.clean('CoAP') )
        
        self.__onConnect( message )


    def __wrapperOnMessage(self, message):
        if( self.__onMessage == None ): return
        
        message = None
        while message == None or message.payload == None:
            if ( self.__isConnectionExpired() ):  self.__reconnect()            
            message = self.__client.get( self.__topics )
        
        result = Message() 
        result.setPayload( StringUtil.clean(message.payload) if message != None else StringUtil.getNoneAsEmpty(None) )
        result.setTopic( StringUtil.clean(self.__topics) )
        result.setProtocol( StringUtil.clean('CoAP') )
       
        self.__onMessage( result )

    
    def __isConnectionExpired(self):
        now = time.time()
        return ( now - self.__timestampConnection ) >= self.__keepAlive


    def __disconnect(self):
        if self.__client == None: return
        self.__client.stop()
        del(self.__client)
        self.__client = None
    
    
    def __reconnect(self):
        if self.__client == None: return
        self.__disconnect()
        self.connect(self.__host, self.__port, self.__keepAlive)
        self.consume()
