import json
import threading
import paho.mqtt.client as mqtt

from util.Logger import Logger
from util.Monitor import Metric
from util.Monitor import Monitor
from util.JsonUtil import JsonUtil
from util.Monitor import MetricType
from util.BrokerClient import Message
from util.StringUtil import StringUtil
from model.vo.Protocol import Protocol
from proxy.BrokerProxy import BrokerProxy
from service.RequestService import RequestService
from model.dao.ConfigurationDAO import ConfigurationDAO

from proxy.BrokerProxy import BrokerProxy
from proxy.monitoring.MonitoringBrokerProxy import MonitoringBrokerProxy
from proxy.logging.LoggingBrokerProxy import LoggingBrokerProxy
from proxy.handling.ExceptionHandlingBrokerProxy import ExceptionHandlingBrokerProxy


class CoatiConsumer(object):
    def __init__(self):
        pass


    def onConnect(self, message):
        metric = Monitor.getInstance().findByName( 'coati_avaliable_info' )
        metric = Metric() if metric == None else metric
        metric.setName( 'coati_avaliable_info' )
        metric.setDescription( 'Coati Broker is available' )
        metric.setType( MetricType.GAUGE )
        metric.setLabels( None )
        metric.setValue( 1 )
        Monitor.getInstance().save( metric )


    def onMessage(self, message):
        pass

    
    def consume(self):
        properties = ConfigurationDAO( 'Coati' )
        address = StringUtil.clean( properties.get('address.broker') )
        port = StringUtil.toInt( properties.get('port.broker') )
        keepAlive = StringUtil.toInt( properties.get('keep.alive.broker') )
        topic = StringUtil.clean( properties.get('topic.subscribe.broker') )

        self.__brokerProxy = BrokerProxy()
        self.__brokerProxy = LoggingBrokerProxy( self.__brokerProxy )
        self.__brokerProxy = MonitoringBrokerProxy( self.__brokerProxy )
        self.__brokerProxy = ExceptionHandlingBrokerProxy( self.__brokerProxy )

        self.__brokerProxy.over( Protocol.COAP )
        self.__brokerProxy.connect( address, port, keepAlive, self.onConnect )
    
