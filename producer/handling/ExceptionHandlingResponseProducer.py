import paho.mqtt.client as mqtt

from util.Logger import Logger
from util.Monitor import Metric
from util.Monitor import Monitor
from util.JsonUtil import JsonUtil
from util.StringUtil import StringUtil
from util.ObjectUtil import ObjectUtil
from util.Monitor import MetricType
from util.StringUtil import StringUtil
from model.dao.ConfigurationDAO import ConfigurationDAO

class ExceptionHandlingResponseProducer(object):
    def __init__(self, responseProducer):
        self.__responseProducer = responseProducer


    def produce(self, response):
        result = None

        try:
            result = self.__responseProducer.produce( response )
        
        except Exception as exception:
            classpath = 'producer.ResponseProducer.produce'
            parameters = StringUtil.clean({ 'response' : StringUtil.clean(response) })
            exceptionMessage = StringUtil.clean(exception)
            messageError = classpath + '  ' + parameters  + '  ' + exceptionMessage
            Logger.error( messageError )

            metric = Monitor.getInstance().findByName( 'app_response_failure_total' )
            metric = Metric() if metric == None else metric
            metric.setName( 'app_response_failure_total' )
            metric.setDescription( 'Total API response failed' )
            metric.setType( MetricType.COUNTER )
            protocol = StringUtil.clean( response.getOverProtocol().name ).upper()
            labels = ObjectUtil.getDefaultIfEmpty( metric.getLabels(), [ ( 'protocol', protocol ) ] )
            metric.setLabels( labels )
            metric.setValue( metric.getValue() + 1 )
            Monitor.getInstance().save( metric )
        
        return result