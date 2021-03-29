from util.Logger import Logger
from util.Monitor import Metric
from util.Monitor import Monitor
from model.Request import Request
from util.JsonUtil import JsonUtil
from util.Monitor import MetricType
from util.StringUtil import StringUtil
from proxy.FiwareOrionProxy import FiwareOrionProxy

class LoggingFiwareOrionProxy(object):
    def __init__(self, fiwareOrionProxy):
        self.__fiwareOrionProxy = fiwareOrionProxy


    def read(self, request):
        classpath = 'proxy.FiwareOrionProxy.read'
        parameters = StringUtil.clean({ 'request' : StringUtil.clean( request ) })
        Logger.debug( classpath + '  ' + parameters )
        self.__fiwareOrionProxy.read( request )


    def create(self, request):
        classpath = 'proxy.FiwareOrionProxy.create'
        parameters = StringUtil.clean({ 'request' : StringUtil.clean( request ) })
        Logger.debug( classpath + '  ' + parameters )
        self.__fiwareOrionProxy.create( request )

    
    def update(self, request):
        classpath = 'proxy.FiwareOrionProxy.update'
        parameters = StringUtil.clean({ 'request' : StringUtil.clean( request ) })
        Logger.debug( classpath + '  ' + parameters )
        self.__fiwareOrionProxy.update( request )

    
    def delete(self, request):
        classpath = 'proxy.FiwareOrionProxy.delete'
        parameters = StringUtil.clean({ 'request' : StringUtil.clean( request ) })
        Logger.debug( classpath + '  ' + parameters )
        self.__fiwareOrionProxy.delete( request )
    
