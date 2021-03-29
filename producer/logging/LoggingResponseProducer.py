from util.Logger import Logger
from util.JsonUtil import JsonUtil
from util.StringUtil import StringUtil
from producer.ResponseProducer import ResponseProducer

class LoggingResponseProducer(object):
    def __init__(self, responseProducer):
        self.__responseProducer = responseProducer


    def produce(self, request):
        classpath = 'producer.ResponseProducer.produce'
        parameters = StringUtil.clean({ 'request' : StringUtil.clean( request ) })
        Logger.debug( classpath + '  ' + parameters )
        result = self.__responseProducer.produce( request )

        return result

