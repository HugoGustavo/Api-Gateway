import time

from util.Logger import Logger
from util.Monitor import Metric
from util.Monitor import Monitor
from util.JsonUtil import JsonUtil
from util.Monitor import MetricType
from util.StringUtil import StringUtil
from model.Response import Response
from producer.ResponseProducer import ResponseProducer

class MonitoringResponseProducer(object):
    def __init__(self, responseProducer):
        self.__responseProducer = responseProducer


    def produce(self, response):
        response.setArriveTime( time.time() )
        self.__responseProducer.produce( response )

