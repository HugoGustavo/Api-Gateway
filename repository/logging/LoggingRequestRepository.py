from util.Logger import Logger
from util.Monitor import Metric
from util.Monitor import Monitor
from util.JsonUtil import JsonUtil
from util.Monitor import MetricType
from util.StringUtil import StringUtil
from repository.RequestRepository import RequestRepository

class LoggingRequestRepository(object):
    def __init__(self, repository):
        self.__repository = repository


    def connect(self):
        classpath = 'repository.RequestRepository.connect'
        parameters = ''
        Logger.debug( classpath + '  ' + parameters )
        result = self.__repository.connect()
        
        return result

    
    def isConnected(self):
        classpath = 'repository.RequestRepository.isConnected'
        parameters = ''
        Logger.debug( classpath + '  ' + parameters )
        result = self.__repository.isConnected()
        
        return result


    def disconnect(self):
        classpath = 'repository.RequestRepository.disconnect'
        parameters = ''
        Logger.debug( classpath + '  ' + parameters )
        result = self.__repository.disconnect()
        
        return result


    def commit(self):
        classpath = 'repository.RequestRepository.commit'
        parameters = ''
        Logger.debug( classpath + '  ' + parameters )
        result = self.__repository.commit()

        return result


    def save(self, request):
        classpath = 'repository.RequestRepository.save'
        parameters = StringUtil.clean({ 'request' : StringUtil.clean( request ) })
        Logger.debug( classpath + '  ' + parameters )
        result = self.__repository.save( request )
        return result


    def findById(self, id):
        classpath = 'repository.RequestRepository.findById'
        parameters = StringUtil.clean({ 'id' : StringUtil.clean( id ) })
        Logger.debug( classpath + '  ' + parameters )
        result = self.__repository.findById( id )
        return result
