import json

from util.Logger import Logger
from model.Request import Request
from util.JsonUtil import JsonUtil
from util.StringUtil import StringUtil
from util.ObjectUtil import ObjectUtil
from util.BrokerClient import Message
from model.vo.Protocol import Protocol
from proxy.BrokerProxy import BrokerProxy
from model.vo.HTTPMethod import HTTPMethod
from service.RequestService import RequestService
from model.dao.ConfigurationDAO import ConfigurationDAO

from proxy.BrokerProxy import BrokerProxy
from proxy.monitoring.MonitoringBrokerProxy import MonitoringBrokerProxy
from proxy.logging.LoggingBrokerProxy import LoggingBrokerProxy
from proxy.handling.ExceptionHandlingBrokerProxy import ExceptionHandlingBrokerProxy

class RequestConsumer(object):
    def __init__(self, requestService):
        self.__requestService = requestService


    def onConnect(self, message):
        pass

    
    def onMessage(self, message):
        request = Request()
        request_json = StringUtil.toJson( message.getPayload() )
        request.setReplyHost( StringUtil.clean(request_json['replyHost']) )
        request.setReplyPort( StringUtil.toInt(request_json['replyPort']) )
        request.setReplyChannel( StringUtil.clean(request_json['replyChannel']) )
        request.setReplyProtocol( Protocol[ StringUtil.clean(request_json['replyProtocol']).upper() ] )
        request.setOverProtocol( Protocol[ StringUtil.clean(message.getProtocol()).upper() ] )
        request.setMethod( HTTPMethod[ StringUtil.clean(request_json['method']).upper() ] )
        request.setUri( StringUtil.clean(request_json['uri']) )
        request.setHeader( StringUtil.clean(request_json['header']) )
        request.setBody( StringUtil.clean(request_json['body']) )
        request.setArriveTime( StringUtil.toFloat(request_json.get('arriveTime', None)) )
        request.setDepartureTime( None )

        self.__requestService.route(request)


    def consume(self):
        properties = ConfigurationDAO( 'RequestMQTT' )
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

        properties = ConfigurationDAO( 'RequestCOAP' )
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