import re
import sqlite3

from model.Request import Request
from model.dao.ConfigurationDAO import ConfigurationDAO
from service.FiwareOrionService import FiwareOrionService
from repository.RequestRepository import RequestRepository

class RequestService(object):
    def __init__(self):
        self.__properties = ConfigurationDAO('ApiGatewayResponse')
        self.__fiwareOrionService = FiwareOrionService()
        
    def save(self, request):
        connection = sqlite3.connect('ApiGateway.db')
        requestRepository = RequestRepository(connection)
        requestSaved = requestRepository.save(request)
        connection.commit()
        connection.close()
        return requestSaved
    
    def findById(self, id):
        connection = sqlite3.connect('ApiGateway.db')
        requestRepository = RequestRepository(connection)
        request = requestRepository.findById(id)
        connection.close()
        return request

    def route(self, request):
        replyHost = request.getReplyHost()
        replyPort = str(request.getReplyPort()).strip()
        replyChannel = request.getReplyChannel()

        if ( replyHost and replyPort and replyChannel ):
            request = self.save(request)
            request.setReplyHost(self.__properties.get('address.broker'))
            request.setReplyPort(self.__properties.get('port.broker'))
            request.setReplyChannel(self.__properties.get('topic.subscribe.broker'))
        
        if ( "GET" == request.getMethod() ): 
            self.__fiwareOrionService.read(request)
        elif ( "POST" == request.getMethod() ): 
            self.__fiwareOrionService.create(request)
        elif ( "PATCH" == request.getMethod() ):
            self.__fiwareOrionService.update(request)
        elif ( "DELETE" == request.getMethod() ):
            self.__fiwareOrionService.delete(request)