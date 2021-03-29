from util.Logger import Logger
from model.Request import Request
from model.Response import Response
from util.StringUtil import StringUtil
from service.RequestService import RequestService
from service.IoTService import IoTService

class ResponseService(object):
    def __init__(self, requestService, iotService):
        self.__requestService = requestService
        self.__iotService = iotService

    
    def route(self, response):
        request = self.__requestService.findById( response.getId() )

        response.setReplyHost( request.getReplyHost() )
        response.setReplyPort( request.getReplyPort() )
        response.setReplyChannel( request.getReplyChannel() )
        response.setReplyProtocol( request.setReplyProtocol() )
        
        self.__iotService.route( response )
