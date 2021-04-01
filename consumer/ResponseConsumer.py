import json

from util.Logger import Logger
from util.JsonUtil import JsonUtil
from model.Response import Response
from util.BrokerClient import Message
from model.vo.Protocol import Protocol
from util.StringUtil import StringUtil
from util.ObjectUtil import ObjectUtil
from proxy.BrokerProxy import BrokerProxy
from service.ResponseService import ResponseService
from model.dao.ConfigurationDAO import ConfigurationDAO

from proxy.BrokerProxy import BrokerProxy
from proxy.monitoring.MonitoringBrokerProxy import MonitoringBrokerProxy
from proxy.logging.LoggingBrokerProxy import LoggingBrokerProxy
from proxy.handling.ExceptionHandlingBrokerProxy import ExceptionHandlingBrokerProxy

class ResponseConsumer(object):
    def __init__(self, responseService):
        self.__responseService = responseService

    def onConnect(self, message):
        pass

    def onMessage(self, message):
        response = Response()
        response_json = StringUtil.toJson( message.getPayload() )
        response.setId( response_json['id'] )
        response.setReplyHost( StringUtil.clean(response_json['replyHost']) )
        response.setReplyPort( StringUtil.toInt(response_json['replyPort']) )
        response.setReplyChannel( StringUtil.clean(response_json['replyChannel']) )
        response.setReplyProtocol( Protocol(StringUtil.clean(response_json['replyProtocol'])) )
        response.setOverProtocol( Protocol[StringUtil.clean(message.getProtocol()).upper()] )
        response.setVersionProtocol( StringUtil.clean(response_json['versionProtocol']) )
        response.setStatusCode( response_json['statusCode'] )
        response.setStatusMessage( StringUtil.clean(response_json['statusMessage']) )
        response.setHeader( StringUtil.clean(response_json['header']) )
        response.setBody( StringUtil.clean(response_json['body']) )
        response.setArriveTime( StringUtil.toFloat(response_json.get('arriveTime', None)) )
        response.setDepartureTime( None )

        self.__responseService.route(response)

    
    def consume(self):
        properties = ConfigurationDAO( 'ResponseMQTT' )
        address = StringUtil.clean( properties.get('address.broker') )
        port = StringUtil.toInt( properties.get('port.broker') )
        keepAlive = StringUtil.toInt( properties.get('keep.alive.broker') )
        topic = StringUtil.clean( properties.get('topic.subscribe.broker') )

        self.__brokerProxy = BrokerProxy()
        self.__brokerProxy = LoggingBrokerProxy( self.__brokerProxy )
        self.__brokerProxy = MonitoringBrokerProxy( self.__brokerProxy )
        self.__brokerProxy = ExceptionHandlingBrokerProxy( self.__brokerProxy )

        self.__brokerProxy.over( Protocol.MQTT )
        self.__brokerProxy.connect( address, port, keepAlive )
        self.__brokerProxy.subscribe( topic, self.onMessage )
        self.__brokerProxy.consume()
       
        properties = ConfigurationDAO( 'ResponseCOAP' )
        address = StringUtil.clean( properties.get('address.broker') )
        port = StringUtil.toInt( properties.get('port.broker') )
        keepAlive = StringUtil.toInt( properties.get('keep.alive.broker') )
        topic = StringUtil.clean( properties.get('topic.subscribe.broker') )

        self.__brokerProxy = BrokerProxy()
        self.__brokerProxy = LoggingBrokerProxy( self.__brokerProxy )
        self.__brokerProxy = MonitoringBrokerProxy( self.__brokerProxy )
        self.__brokerProxy = ExceptionHandlingBrokerProxy( self.__brokerProxy )

        self.__brokerProxy.over( Protocol.COAP )
        self.__brokerProxy.connect( address, port, keepAlive )
        self.__brokerProxy.subscribe( topic, self.onMessage )
        self.__brokerProxy.consume()