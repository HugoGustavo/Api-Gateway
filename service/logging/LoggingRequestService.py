from util.Logger import Logger
from util.Monitor import Metric
from util.Monitor import Monitor
from util.JsonUtil import JsonUtil
from util.Monitor import MetricType
from util.StringUtil import StringUtil
from util.ObjectUtil import ObjectUtil
from service.RequestService import RequestService

class LoggingRequestService(object):
    def __init__(self, requestService):
        self.__requestService = requestService


    def save(self, request):
        classpath = 'service.RequestService.save'
        parameters = StringUtil.clean({ 'request' : StringUtil.clean( request ) })
        Logger.debug( classpath + '  ' + parameters )
        result = self.__requestService.save( request )
        
        return result


    def findById(self, id):
        classpath = 'service.RequestService.findById'
        parameters = StringUtil.clean({ 'id' : StringUtil.clean( id ) })
        Logger.debug( classpath + '  ' + parameters )
        result = self.__requestService.findById( id )
        
        return result 


    def route(self, request):
        classpath = 'service.RequestService.route'
        parameters = StringUtil.clean({ 'request' : StringUtil.clean( request ) })
        Logger.debug( classpath + '  ' + parameters )
        result = self.__requestService.route( request )

        return result
    
