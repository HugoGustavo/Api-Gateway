import json
import requests

from util.Logger import Logger
from model.Request import Request
from model.Response import Response
from util.VM9ITConnection import VM9ITConnection
from producer.ResponseProducer import ResponseProducer
from model.dao.ConfigurationDAO import ConfigurationDAO


class VM9ITService(object):
    def __init__(self):
        self.__properties = ConfigurationDAO('VM9IT')
        self.__address = self.__properties.get('address')
        self.__port = self.__properties.get('port')
        self.__url = 'http://' + self.__address + ':' + self.__port
        self.__responseProducer = ResponseProducer()

    def read(self, request):
        vm9itConnection = VM9ITConnection()
        header = vm9itConnection.getHeader()
        responseGet = requests.get(self.__url + request.getUri(), headers=header)

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
        vm9itConnection = VM9ITConnection()
        header = vm9itConnection.getHeader()

        body = json.loads(request.getBody().replace("'", '"'))
        responsePost = requests.post(self.__url + request.getUri(), json=body, headers=header)

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
        vm9itConnection = VM9ITConnection()
        header = vm9itConnection.getHeader()

        body = json.loads(request.getBody().replace("'", '"'))
        responsePut = requests.put(self.__url + request.getUri(), json=body, headers=header)

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
        vm9itConnection = VM9ITConnection()
        header = vm9itConnection.getHeader()

        responseDelete = requests.delete(self.__url + request.getUri(), headers=header)

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