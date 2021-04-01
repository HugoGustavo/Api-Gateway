import re
import sqlite3

from util.Logger import Logger
from model.Request import Request
from util.StringUtil import StringUtil
from util.ObjectUtil import ObjectUtil
from model.vo.Protocol import Protocol
from model.vo.HTTPMethod import HTTPMethod
from model.dao.ConfigurationDAO import ConfigurationDAO
from service.FiwareOrionService import FiwareOrionService
from repository.RequestRepository import RequestRepository

class RequestService(object):
    def __init__(self, requestRepository, fiwareOrionService):
        self.__properties = ConfigurationDAO( 'RequestMQTT' )
        self.__requestRepository = requestRepository
        self.__fiwareOrionService = fiwareOrionService
        
    
    def save(self, request):
        self.__requestRepository.connect()
        requestSaved = self.__requestRepository.save( request )
        self.__requestRepository.commit()
        self.__requestRepository.disconnect()
        return requestSaved
    
    
    def findById(self, id):
        self.__requestRepository.connect()
        request = self.__requestRepository.findById( id )
        self.__requestRepository.disconnect()
        return request

    
    def route(self, request):
        replyHost = request.getReplyHost()
        replyPort = StringUtil.clean( request.getReplyPort() )
        replyChannel = request.getReplyChannel()
        replyProtocol = request.getReplyProtocol()

        if ( replyHost and replyPort and replyChannel and replyProtocol ):
            request = self.save( request )
            request.setReplyHost( self.__properties.get('address.broker') )
            request.setReplyPort( self.__properties.get('port.broker') )
            request.setReplyChannel( self.__properties.get('topic.subscribe.broker') )
            request.setReplyProtocol( replyProtocol )
        
        if ( request.getMethod() == HTTPMethod.GET ):
            self.__fiwareOrionService.read( request )
        elif ( request.getMethod() == HTTPMethod.POST ):
            self.__fiwareOrionService.create( request )
        elif ( request.getMethod() == HTTPMethod.PATCH ):
            self.__fiwareOrionService.update( request )
        elif ( request.getMethod() == HTTPMethod.DELETE ):
            self.__fiwareOrionService.delete( request )