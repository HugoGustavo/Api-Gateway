import json
import requests

from model.Request import Request
from model.Response import Response
from util.VM9ITConnection import VM9ITConnection
from producer.ResponseProducer import ResponseProducer

class VM9ITService(object):
    def __init__(self):
        self.__responseProducer = ResponseProducer()
        self.__vm9itConnection = VM9ITConnection()

    def read(self, request):
        responseGet = self.__vm9itConnection.doGet(request.getUri())

        response = Response()
        response.setId(request.getId())
        response.setReplyHost(str(request.getReplyHost()))
        response.setReplyPort(int(request.getReplyPort()))
        response.setReplyChannel(str(request.getReplyChannel()))
        response.setVersionProtocol('HTTP/1.0' if responseGet.raw.version == 10 else 'HTTP/1.1')
        response.setStatusCode(int(responseGet.status_code))
        response.setStatusMessage(str(responseGet.reason))
        response.setHeader(str(responseGet.headers))
        response.setBody(str(responseGet.text))

        self.__responseProducer.produce(response) 
    
    def create(self, request):
        responsePost = self.__vm9itConnection.doPost(request.getUri(), request.getBody())

        response = Response()
        response.setId(request.getId())
        response.setReplyHost(str(request.getReplyHost()))
        response.setReplyPort(int(request.getReplyPort()))
        response.setReplyChannel(str(request.getReplyChannel()))
        response.setVersionProtocol('HTTP/1.0' if responsePost.raw.version == 10 else 'HTTP/1.1')
        response.setStatusCode(int(responsePost.status_code))
        response.setStatusMessage(str(responsePost.reason))
        response.setHeader(str(responsePost.headers))
        response.setBody(str(responsePost.text))

        self.__responseProducer.produce(response)

    def update(self, request):
        responsePut = self.__vm9itConnection.doPut(request.getUri(), request.getBody())

        response = Response()
        response.setId(request.getId())
        response.setReplyHost(str(request.getReplyHost()))
        response.setReplyPort(int(request.getReplyPort()))
        response.setReplyChannel(str(request.getReplyChannel()))
        response.setVersionProtocol('HTTP/1.0' if responsePut.raw.version == 10 else 'HTTP/1.1')
        response.setStatusCode(int(responsePut.status_code))
        response.setStatusMessage(str(responsePut.reason))
        response.setHeader(str(responsePut.headers))
        response.setBody(str(responsePut.text))

        self.__responseProducer.produce(response)

    def delete(self, request):
        responseDelete = self.__vm9itConnection.doDelete(request.getUri())

        response = Response()
        response.setId(request.getId())
        response.setReplyHost(str(request.getReplyHost()))
        response.setReplyPort(int(request.getReplyPort()))
        response.setReplyChannel(str(request.getReplyChannel()))
        response.setVersionProtocol('HTTP/1.0' if responseDelete.raw.version == 10 else 'HTTP/1.1')
        response.setStatusCode(int(responseDelete.status_code))
        response.setStatusMessage(str(responseDelete.reason))
        response.setHeader(str(responseDelete.headers))
        response.setBody(str(responseDelete.text))

        self.__responseProducer.produce(response) 