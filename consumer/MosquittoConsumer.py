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


class MosquittoConsumer(object):
    def __init__(self):
        pass

    def onConnect(self, message):
        metric = Monitor.getInstance().findByName( 'mosquitto_avaliable_info' )
        metric = Metric() if metric == None else metric
        metric.setName( 'mosquitto_avaliable_info' )
        metric.setDescription( 'Mosquito Broker is available' )
        metric.setType( MetricType.GAUGE )
        metric.setLabels( None )
        metric.setValue( 1 )
        Monitor.getInstance().save( metric )


    def onMessage(self, message):
        if( '$SYS/broker/version' == message.getTopic() ):
            metric = Monitor.getInstance().findByName( 'mosquitto_version' )
            metric = Metric() if metric == None else metric
            metric.setName( 'mosquitto_version' )
            metric.setDescription( 'The version of the Mosquitto Broker' )
            metric.setType( MetricType.GAUGE )
            labels = [ ('version', StringUtil.clean( message.payload )[20:-1]) ]
            metric.setLabels( labels )
            metric.setValue( 1.0 )
            Monitor.getInstance().save( metric )

        if( '$SYS/broker/uptime' == message.getTopic() ):
            metric = Monitor.getInstance().findByName( 'mosquitto_uptime_seconds' )
            metric = Metric() if metric == None else metric
            metric.setName( 'mosquitto_uptime_seconds' )
            metric.setDescription( 'The uptime of the Mosquitto Broker' )
            metric.setType( MetricType.GAUGE )
            metric.setLabels( None )
            value = StringUtil.clean( message.payload )
            value = StringUtil.substring(value, 2, -9)
            value = StringUtil.toInt( value )
            metric.setValue( value )
            Monitor.getInstance().save( metric )

        if( '$SYS/broker/clients/total' == message.getTopic() ):
            metric = Monitor.getInstance().findByName( 'mosquitto_clients_total' )
            metric = Metric() if metric == None else metric
            metric.setName( 'mosquitto_clients_total' )
            metric.setDescription( 'The total number of active and inactive clients currently connected and registered on the broker.' )
            metric.setType( MetricType.GAUGE )
            metric.setLabels( None )
            value = StringUtil.clean( message.payload )
            value = StringUtil.substring(value, 2, -1)
            value = StringUtil.toInt( value )
            metric.setValue( value )
            Monitor.getInstance().save( metric )

        if( '$SYS/broker/clients/active' == message.getTopic() ):
            metric = Monitor.getInstance().findByName( 'mosquitto_clients_active_total' )
            metric = Metric() if metric == None else metric
            metric.setName( 'mosquitto_clients_active_total' )
            metric.setDescription( 'The total number of active clients currently connected and registered on the broker.' )
            metric.setType( MetricType.GAUGE )
            metric.setLabels( None )
            value = StringUtil.clean( message.payload )
            value = StringUtil.substring(value, 2, -1)
            value = StringUtil.toInt( value )
            metric.setValue( value )
            Monitor.getInstance().save( metric )

        if( '$SYS/broker/clients/connected' == message.getTopic() ):
            metric = Monitor.getInstance().findByName( 'mosquitto_clients_connected_total' )
            metric = Metric() if metric == None else metric
            metric.setName( 'mosquitto_clients_connected_total' )
            metric.setDescription( 'The total number of clients currently connected and registered on the broker.' )
            metric.setType( MetricType.GAUGE )
            metric.setLabels( None )
            value = StringUtil.clean( message.payload )
            value = StringUtil.substring(value, 2, -1)
            value = StringUtil.toInt( value )
            metric.setValue( value )
            Monitor.getInstance().save( metric )

        if( '$SYS/broker/load/messages/received/1min' == message.getTopic() ):
            metric = Monitor.getInstance().findByName( 'mosquitto_messages_received_1min_total_total' )
            metric = Metric() if metric == None else metric
            metric.setName( 'mosquitto_messages_received_1min_total_total' )
            metric.setDescription( 'The moving average of the number of all types of MQTT messages received in 1 min.' )
            metric.setType( MetricType.GAUGE )
            metric.setLabels( None )
            value = StringUtil.clean( message.payload )
            value = StringUtil.substring(value, 2, -1)
            value = StringUtil.toFloat( value )
            metric.setValue( value )
            Monitor.getInstance().save( metric )

        if( '$SYS/broker/load/messages/received/5min' == message.getTopic() ):
            metric = Monitor.getInstance().findByName( 'mosquitto_messages_received_5min_total_total' )
            metric = Metric() if metric == None else metric
            metric.setName( 'mosquitto_messages_received_5min_total_total' )
            metric.setDescription( 'The moving average of the number of all types of MQTT messages received in 5 min.' )
            metric.setType( MetricType.GAUGE )
            metric.setLabels( None )
            value = StringUtil.clean( message.payload )
            value = StringUtil.substring(value, 2, -1)
            value = StringUtil.toFloat( value )
            metric.setValue( value )
            Monitor.getInstance().save( metric )

        if( '$SYS/broker/load/messages/received/15min' == message.getTopic() ):
            metric = Monitor.getInstance().findByName( 'mosquitto_messages_received_15min_total' )
            metric = Metric() if metric == None else metric
            metric.setName( 'mosquitto_messages_received_15min_total' )
            metric.setDescription( 'The moving average of the number of all types of MQTT messages received in 15 min.' )
            metric.setType( MetricType.GAUGE )
            metric.setLabels( None )
            value = StringUtil.clean( message.payload )
            value = StringUtil.substring(value, 2, -1)
            value = StringUtil.toFloat( value )
            metric.setValue( value )
            Monitor.getInstance().save( metric )

        if( '$SYS/broker/load/messages/sent/1min' == message.getTopic() ):
            metric = Monitor.getInstance().findByName( 'mosquitto_messages_sent_1min_total' )
            metric = Metric() if metric == None else metric
            metric.setName( 'mosquitto_messages_sent_1min_total' )
            metric.setDescription( 'The moving average of the number of all types of MQTT messages sent in 1 min.' )
            metric.setType( MetricType.GAUGE )
            metric.setLabels( None )
            value = StringUtil.clean( message.payload )
            value = StringUtil.substring(value, 2, -1)
            value = StringUtil.toFloat( value )
            metric.setValue( value )
            Monitor.getInstance().save( metric )

        if( '$SYS/broker/load/messages/sent/5min' == message.getTopic() ):
            metric = Monitor.getInstance().findByName( 'mosquitto_messages_sent_5min_total' )
            metric = Metric() if metric == None else metric
            metric.setName( 'mosquitto_messages_sent_5min_total' )
            metric.setDescription( 'The moving average of the number of all types of MQTT messages sent in 5 min.' )
            metric.setType( MetricType.GAUGE )
            metric.setLabels( None )
            value = StringUtil.clean( message.payload )
            value = StringUtil.substring(value, 2, -1)
            value = StringUtil.toFloat( value )
            metric.setValue( value )
            Monitor.getInstance().save( metric )

        if( '$SYS/broker/load/messages/sent/15min' == message.getTopic() ):
            metric = Monitor.getInstance().findByName( 'mosquitto_messages_sent_15min_total' )
            metric = Metric() if metric == None else metric
            metric.setName( 'mosquitto_messages_sent_15min_total' )
            metric.setDescription( 'The moving average of the number of all types of MQTT messages sent in 15 min.' )
            metric.setType( MetricType.GAUGE )
            metric.setLabels( None )
            value = StringUtil.clean( message.payload )
            value = StringUtil.substring(value, 2, -1)
            value = StringUtil.toFloat( value )
            metric.setValue( value )
            Monitor.getInstance().save( metric )

        if( '$SYS/broker/load/bytes/received/1min' == message.getTopic() ):
            metric = Monitor.getInstance().findByName( 'mosquitto_bytes_received_1min_total' )
            metric = Metric() if metric == None else metric
            metric.setName( 'mosquitto_bytes_received_1min_total' )
            metric.setDescription( 'The moving average of the number of bytes received by the broker over 1 min.' )
            metric.setType( MetricType.GAUGE )
            metric.setLabels( None )
            value = StringUtil.clean( message.payload )
            value = StringUtil.substring(value, 2, -1)
            value = StringUtil.toFloat( value )
            metric.setValue( value )
            Monitor.getInstance().save( metric )
            
        if( '$SYS/broker/load/bytes/received/5min' == message.getTopic() ):
            metric = Monitor.getInstance().findByName( 'mosquitto_bytes_received_5min_total' )
            metric = Metric() if metric == None else metric
            metric.setName( 'mosquitto_bytes_received_5min_total' )
            metric.setDescription( 'The moving average of the number of bytes received by the broker over 5 min.' )
            metric.setType( MetricType.GAUGE )
            metric.setLabels( None )
            value = StringUtil.clean( message.payload )
            value = StringUtil.substring(value, 2, -1)
            value = StringUtil.toFloat( value )
            metric.setValue( value )
            Monitor.getInstance().save( metric )

        if( '$SYS/broker/load/bytes/received/15min' == message.getTopic() ):
            metric = Monitor.getInstance().findByName( 'mosquitto_bytes_received_15min_total' )
            metric = Metric() if metric == None else metric
            metric.setName( 'mosquitto_bytes_received_15min_total' )
            metric.setDescription( 'The moving average of the number of bytes received by the broker over 15 min.' )
            metric.setType( MetricType.GAUGE )
            metric.setLabels( None )
            value = StringUtil.clean( message.payload )
            value = StringUtil.substring(value, 2, -1)
            value = StringUtil.toFloat( value )
            metric.setValue( value )
            Monitor.getInstance().save( metric )

        if( '$SYS/broker/load/bytes/sent/1min' == message.getTopic() ):
            metric = Monitor.getInstance().findByName( 'mosquitto_bytes_sent_1min_total' )
            metric = Metric() if metric == None else metric
            metric.setName( 'mosquitto_bytes_sent_1min_total' )
            metric.setDescription( 'The moving average of the number of bytes sent by the broker over 1 min.' )
            metric.setType( MetricType.GAUGE )
            metric.setLabels( None )
            value = StringUtil.clean( message.payload )
            value = StringUtil.substring(value, 2, -1)
            value = StringUtil.toFloat( value )
            metric.setValue( value )
            Monitor.getInstance().save( metric )

        if( '$SYS/broker/load/bytes/sent/5min' == message.getTopic() ):
            metric = Monitor.getInstance().findByName( 'mosquitto_bytes_sent_5min_total' )
            metric = Metric() if metric == None else metric
            metric.setName( 'mosquitto_bytes_sent_5min_total' )
            metric.setDescription( 'The moving average of the number of bytes sent by the broker over 5 min.' )
            metric.setType( MetricType.GAUGE )
            metric.setLabels( None )
            value = StringUtil.clean( message.payload )
            value = StringUtil.substring(value, 2, -1)
            value = StringUtil.toFloat( value )
            metric.setValue( value )
            Monitor.getInstance().save( metric )

        if( '$SYS/broker/load/bytes/sent/15min' == message.getTopic() ):
            metric = Monitor.getInstance().findByName( 'mosquitto_bytes_sent_15min_total' )
            metric = Metric() if metric == None else metric
            metric.setName( 'mosquitto_bytes_sent_15min_total' )
            metric.setDescription( 'The moving average of the number of bytes sent by the broker over 15 min.' )
            metric.setType( MetricType.GAUGE )
            metric.setLabels( None )
            value = StringUtil.clean( message.payload )
            value = StringUtil.substring(value, 2, -1)
            value = StringUtil.toFloat( value )
            metric.setValue( value )
            Monitor.getInstance().save( metric )

        if( '$SYS/broker/load/sockets/1min' == message.getTopic() ):
            metric = Monitor.getInstance().findByName( 'mosquitto_sockets_opened_1min_total' )
            metric = Metric() if metric == None else metric
            metric.setName( 'mosquitto_sockets_opened_1min_total' )
            metric.setDescription( 'The moving average of the number of socket connections opened to the broker over 1 min.' )
            metric.setType( MetricType.GAUGE )
            metric.setLabels( None )
            value = StringUtil.clean( message.payload )
            value = StringUtil.substring(value, 2, -1)
            value = StringUtil.toFloat( value )
            metric.setValue( value )
            Monitor.getInstance().save( metric )

        if( '$SYS/broker/load/sockets/5min' == message.getTopic() ):
            metric = Monitor.getInstance().findByName( 'mosquitto_sockets_opened_5min_total' )
            metric = Metric() if metric == None else metric
            metric.setName( 'mosquitto_sockets_opened_5min_total' )
            metric.setDescription( 'The moving average of the number of socket connections opened to the broker over 5 min.' )
            metric.setType( MetricType.GAUGE )
            metric.setLabels( None )
            value = StringUtil.clean( message.payload )
            value = StringUtil.substring(value, 2, -1)
            value = StringUtil.toFloat( value )
            metric.setValue( value )
            Monitor.getInstance().save( metric )

        if( '$SYS/broker/load/sockets/15min' == message.getTopic() ):
            metric = Monitor.getInstance().findByName( 'mosquitto_sockets_opened_15min_total' )
            metric = Metric() if metric == None else metric
            metric.setName( 'mosquitto_sockets_opened_15min_total' )
            metric.setDescription( 'The moving average of the number of socket connections opened to the broker over 15 min.' )
            metric.setType( MetricType.GAUGE )
            metric.setLabels( None )
            value = StringUtil.clean( message.payload )
            value = StringUtil.substring(value, 2, -1)
            value = StringUtil.toFloat( value )
            metric.setValue( value )
            Monitor.getInstance().save( metric )

        if( '$SYS/broker/load/connections/1min' == message.getTopic() ):
            metric = Monitor.getInstance().findByName( 'mosquitto_connect_packets_1min_total' )
            metric = Metric() if metric == None else metric
            metric.setName( 'mosquitto_connect_packets_1min_total' )
            metric.setDescription( 'The moving average of the number of CONNECT packets received by the broker over 1 min.' )
            metric.setType( MetricType.GAUGE )
            metric.setLabels( None )
            value = StringUtil.clean( message.payload )
            value = StringUtil.substring(value, 2, -1)
            value = StringUtil.toFloat( value )
            metric.setValue( value )
            Monitor.getInstance().save( metric )

        if( '$SYS/broker/load/connections/5min' == message.getTopic() ):
            metric = Monitor.getInstance().findByName( 'mosquitto_connect_packets_5min_total' )
            metric = Metric() if metric == None else metric
            metric.setName( 'mosquitto_connect_packets_5min_total' )
            metric.setDescription( 'The moving average of the number of CONNECT packets received by the broker over 5 min.' )
            metric.setType( MetricType.GAUGE )
            metric.setLabels( None )
            value = StringUtil.clean( message.payload )
            value = StringUtil.substring(value, 2, -1)
            value = StringUtil.toFloat( value )
            metric.setValue( value )
            Monitor.getInstance().save( metric )

        if( '$SYS/broker/load/connections/15min' == message.getTopic() ):
            metric = Monitor.getInstance().findByName( 'mosquitto_connect_packets_15min_total' )
            metric = Metric() if metric == None else metric
            metric.setName( 'mosquitto_connect_packets_15min_total' )
            metric.setDescription( 'The moving average of the number of CONNECT packets received by the broker over 15 min.' )
            metric.setType( MetricType.GAUGE )
            metric.setLabels( None )
            value = StringUtil.clean( message.payload )
            value = StringUtil.substring(value, 2, -1)
            value = StringUtil.toFloat( value )
            metric.setValue( value )
            Monitor.getInstance().save( metric )

        if( '$SYS/broker/messages/received' == message.getTopic() ):
            metric = Monitor.getInstance().findByName( 'mosquitto_message_received_total' )
            metric = Metric() if metric == None else metric
            metric.setName( 'mosquitto_message_received_total' )
            metric.setDescription( 'The total number of messages of any type received since the broker started.' )
            metric.setType( MetricType.GAUGE )
            metric.setLabels( None )
            value = StringUtil.clean( message.payload )
            value = StringUtil.substring(value, 2, -1)
            value = StringUtil.toFloat( value )
            metric.setValue( value )
            Monitor.getInstance().save( metric )

        if( '$SYS/broker/messages/sent' == message.getTopic() ):
            metric = Monitor.getInstance().findByName( 'mosquitto_message_sent_total' )
            metric = Metric() if metric == None else metric
            metric.setName( 'mosquitto_message_sent_total' )
            metric.setDescription( 'The total number of messages of any type sent since the broker started.' )
            metric.setType( MetricType.GAUGE )
            metric.setLabels( None )
            value = StringUtil.clean( message.payload )
            value = StringUtil.substring(value, 2, -1)
            value = StringUtil.toFloat( value )
            metric.setValue( value )
            Monitor.getInstance().save( metric )

        if( '$SYS/broker/store/messages/bytes' == message.getTopic() ):
            metric = Monitor.getInstance().findByName( 'mosquitto_payload_retained_queued_bytes_total' )
            metric = Metric() if metric == None else metric
            metric.setName( 'mosquitto_payload_retained_queued_bytes_total' )
            metric.setDescription( 'The total number of bytes in payloads of retained and queued messages.' )
            metric.setType( MetricType.GAUGE )
            metric.setLabels( None )
            value = StringUtil.clean( message.payload )
            value = StringUtil.substring(value, 2, -1)
            value = StringUtil.toFloat( value )
            metric.setValue( value )
            Monitor.getInstance().save( metric )

        if( '$SYS/broker/subscriptions/count' == message.getTopic() ):
            metric = Monitor.getInstance().findByName( 'mosquitto_subscriptions_active_total' )
            metric = Metric() if metric == None else metric
            metric.setName( 'mosquitto_subscriptions_active_total' )
            metric.setDescription( 'The total number of subscriptions active on the broker.' )
            metric.setType( MetricType.GAUGE )
            metric.setLabels( None )
            value = StringUtil.clean( message.payload )
            value = StringUtil.substring(value, 2, -1)
            value = StringUtil.toFloat( value )
            metric.setValue( value )
            Monitor.getInstance().save( metric )

        if( '$SYS/broker/heap/current' == message.getTopic() ):
            metric = Monitor.getInstance().findByName( 'mosquitto_size_heap_memory_used_total' )
            metric = Metric() if metric == None else metric
            metric.setName( 'mosquitto_size_heap_memory_used_total' )
            metric.setDescription( 'The current size of the heap memory in use by mosquitto. ' )
            metric.setType( MetricType.GAUGE )
            metric.setLabels( None )
            value = StringUtil.clean( message.payload )
            value = StringUtil.substring(value, 2, -1)
            value = StringUtil.toFloat( value )
            metric.setValue( value )
            Monitor.getInstance().save( metric )

        if( '$SYS/broker/bytes/received' == message.getTopic() ):
            metric = Monitor.getInstance().findByName( 'mosquitto_received_bytes_total' )
            metric = Metric() if metric == None else metric
            metric.setName( 'mosquitto_received_bytes_total' )
            metric.setDescription( 'The total number of bytes received since the broker started.' )
            metric.setType( MetricType.GAUGE )
            metric.setLabels( None )
            value = StringUtil.clean( message.payload )
            value = StringUtil.substring(value, 2, -1)
            value = StringUtil.toFloat( value )
            metric.setValue( value )
            Monitor.getInstance().save( metric )
            
        if( '$SYS/broker/bytes/sent' == message.getTopic() ):
            metric = Monitor.getInstance().findByName( 'mosquitto_sent_bytes_total' )
            metric = Metric() if metric == None else metric
            metric.setName( 'mosquitto_sent_bytes_total' )
            metric.setDescription( 'The total number of bytes sent since the broker started.' )
            metric.setType( MetricType.GAUGE )
            metric.setLabels( None )
            value = StringUtil.clean( message.payload )
            value = StringUtil.substring(value, 2, -1)
            value = StringUtil.toFloat( value )
            metric.setValue( value )
            Monitor.getInstance().save( metric )

    
    def consume(self):
        properties = ConfigurationDAO( 'Mosquitto' )
        address = StringUtil.clean( properties.get('address.broker') )
        port = StringUtil.toInt( properties.get('port.broker') )
        keepAlive = StringUtil.toInt( properties.get('keep.alive.broker') )
        topic = StringUtil.clean( properties.get('topic.subscribe.broker') )

        self.__brokerProxy = BrokerProxy()
        self.__brokerProxy = LoggingBrokerProxy( self.__brokerProxy )
        self.__brokerProxy = MonitoringBrokerProxy( self.__brokerProxy )
        self.__brokerProxy = ExceptionHandlingBrokerProxy( self.__brokerProxy )

        self.__brokerProxy.over( Protocol.MQTT )
        self.__brokerProxy.connect( address, port, keepAlive, self.onConnect )
        self.__brokerProxy.subscribe( topic, self.onMessage )
        self.__brokerProxy.consume()
    
