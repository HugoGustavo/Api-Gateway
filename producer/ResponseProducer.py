from model.Response import Response
from util.StringUtil import StringUtil
from proxy.BrokerProxy import BrokerProxy
from model.dao.ConfigurationDAO import ConfigurationDAO

from proxy.BrokerProxy import BrokerProxy
from proxy.monitoring.MonitoringBrokerProxy import MonitoringBrokerProxy
from proxy.logging.LoggingBrokerProxy import LoggingBrokerProxy
from proxy.handling.ExceptionHandlingBrokerProxy import ExceptionHandlingBrokerProxy

class ResponseProducer(object):
    def __init__(self):
        pass

    def produce(self, response):
        if( response == None ): return

        protocol = ObjectUtil.getDefaultIfNone( response.getOverProtocol(), Protocol.MQTT )
        properties = ConfigurationDAO( 'ResponseMQTT' if protocol == Protocol.MQTT else 'ResponseCOAP' )
        address = StringUtil.clean( properties.get('address.broker') )
        port = StringUtil.toInt( properties.get('port.broker') )
        keepAlive = StringUtil.toInt( properties.get('keep.alive.broker') )
        topic = StringUtil.clean( properties.get('topic.subscribe.broker') )
        payload = StringUtil.clean( response )

        self.__brokerProxy = BrokerProxy()
        self.__brokerProxy = LoggingBrokerProxy( self.__brokerProxy )
        self.__brokerProxy = MonitoringBrokerProxy( self.__brokerProxy )
        self.__brokerProxy = ExceptionHandlingBrokerProxy( self.__brokerProxy )

        self.__brokerProxy.over( protocol )
        self.__brokerProxy.connect( address, port, keepAlive )
        self.__brokerProxy.publish( topic, payload )
