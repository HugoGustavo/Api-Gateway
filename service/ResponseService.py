from model.Request import Request
from model.Response import Response
from service.RequestService import RequestService
from service.ArduinoService import ArduinoService

class ResponseService(object):
    def __init__(self):
        self.__requestService = RequestService()
        self.__arduinoService = ArduinoService()

    def route(self, response):
        request = self.__requestService.findById(response.getId())

        response.setReplyHost(request.getReplyHost())
        response.setReplyPort(request.getReplyPort())
        response.setReplyChannel(request.getReplyChannel())
        
        self.__arduinoService.route(response)
