import json
import enum
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
        return str( json.dumps(self.__dict__) )


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
        host = StringUtil.getNoneAsEmpty( host )
        host = StringUtil.clean( host )
        port = StringUtil.getNoneAsEmpty( port )
        port = StringUtil.clean( port )
        port = StringUtil.toInt( port )
        #path = StringUtil.clean( "/.well-known/core?rt=core.ps" )
        server = ( host, port )
        
        self.__client = HelperClient( server=server )
        #response = self.__client.get( path )
        #response = response.pretty_print()
        #response = str(response)
        #Logger.debug( 'OK1111111111111' + str(response) )
        
        self.__wrapperOnConnect( None )


    def publish(self, topics=None, message=None):
        if self.__client == None: return None
        
        topics = StringUtil.getNoneAsEmpty( topics )
        topics = StringUtil.clean( topics )
        topics = StringUtil.split( topics, "/" )
        subPath = ListUtil.of( "ps" )
        contentType = { 'content_type': defines.Content_types["application/link-format"] }
        for topic in topics:
            path = StringUtil.joinBy( subPath, "/" )
            path = StringUtil.concat( "/", path )
            path = StringUtil.concat( path, "/" )
            body = StringUtil.concat( "<", topic )
            body = StringUtil.concat( topic, ">;ct=40" )
            response = self.__client.post( path , body, None, None, **contentType)
            subPath = ListUtil.append( subPath, topic )

        path = StringUtil.joinBy( subPath, "/" )
        path = StringUtil.concat( "/", path )
        path = StringUtil.concat( path, "/" )
        message = StringUtil.getNoneAsEmpty( message )
        response = self.__client.put( path, message )
        
        return response

    def subscribe(self, topics=None):
        self.__topics = StringUtil.getNoneAsEmpty( topics )
        self.__topics = StringUtil.clean( self.__topics )
        self.__topics = "/ps/" + self.__topics
        self.__topics = StringUtil.replace( self.__topics, "//", "/" )
        self.__topics = StringUtil.clean( self.__topics )
        

    def loopForever(self):
        response = self.__client.observe( self.__topics, callback=self.__wrapperOnMessage )
        return response

    
    def consume(self):
        result = self.loopForever()
        return result


    def getOnMessage(self):
        return self.__onMessage
    

    def setOnMessage(self, onMessage):
        self.__onMessage = onMessage
    

    def getOnConnect(self):
        return self.__onConnect

    
    def setOnConnect(self, onConnect):
        self.__onConnect = onConnect

    
    def __wrapperOnMessage(self, message):
        if ( message == None ): return 
        
        if( self.__onMessage == None ): return

        message = self.__client.get( self.__topics )
        message = message.pretty_print()
        
        result = Message()
        result.setPayload( message )
        result.setTopic( StringUtil.clean(self.__topics) )
        result.setProtocol( StringUtil.clean('CoAP') )
       
        self.__onMessage( result )

    
    def __wrapperOnConnect(self, message):
        if ( message == None ): return 

        if( self.__onConnect == None ): return

        result = Message()
        result.setPayload( StringUtil.getNoneAsEmpty(None) )
        result.setTopic( StringUtil.getNoneAsEmpty(None) )
        result.setProtocol( StringUtil.clean('CoAP') )
        
        self.__onConnect( message )