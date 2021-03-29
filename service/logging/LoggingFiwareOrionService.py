from util.Logger import Logger
from util.Monitor import Metric
from util.Monitor import Monitor
from util.JsonUtil import JsonUtil
from util.Monitor import MetricType
from util.StringUtil import StringUtil
from service.FiwareOrionService import FiwareOrionService

class LoggingFiwareOrionService(object):
    def __init__(self, fiwareOrionService):
        self.__fiwareOrionService = fiwareOrionService


    def read(self, request):
        classpath = 'service.FiwareOrionService.read'
        parameters = StringUtil.clean({ 'request' : StringUtil.clean( request ) })
        Logger.debug( classpath + '  ' + parameters )
        self.__fiwareOrionService.read( request )


    def create(self, request):
        classpath = 'service.FiwareOrionService.create'
        parameters = StringUtil.clean({ 'request' : StringUtil.clean( request ) })
        Logger.debug( classpath + '  ' + parameters )
        self.__fiwareOrionService.create( request )

    
    def update(self, request):
        classpath = 'service.FiwareOrionService.update'
        parameters = StringUtil.clean({ 'request' : StringUtil.clean( request ) })
        Logger.debug( classpath + '  ' + parameters )
        self.__fiwareOrionService.update( request )

    
    def delete(self, request):
        classpath = 'service.FiwareOrionService.delete'
        parameters = StringUtil.clean({ 'request' : StringUtil.clean( request ) })
        Logger.debug( classpath + '  ' + parameters )
        self.__fiwareOrionService.delete( request )
    
