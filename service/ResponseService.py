from util.Logger import Logger
from model.Request import Request
from model.Response import Response
from util.StringUtil import StringUtil
from service.RequestService import RequestService
from service.ArduinoService import ArduinoService

class ResponseService(object):
    def __init__(self, requestService, arduinoService):
        self.__requestService = requestService
        self.__arduinoService = arduinoService

    
    def route(self, response):
        request = self.__requestService.findById( response.getId() )

        response.setReplyHost( request.getReplyHost() )
        response.setReplyPort( request.getReplyPort() )
        response.setReplyChannel( request.getReplyChannel() )
        
        self.__arduinoService.route( response )
