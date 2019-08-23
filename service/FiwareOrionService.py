import json
import requests

from model.Request import Request
from model.Response import Response
from producer.ResponseProducer import ResponseProducer
from model.dao.ConfigurationDAO import ConfigurationDAO


class FiwareOrionService(object):
    def __init__(self):
        self.__properties = ConfigurationDAO('FiwareOrionBroker')
        self.__address = self.__properties.get('address')
        self.__port = self.__properties.get('port')
        self.__url = 'http://' + self.__address + ':' + self.__port + '/v2'
        self.__responseProducer = ResponseProducer()

    def read(self, request):
        responseGet = requests.get(self.__url + request.getUri())

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
        body = json.loads(request.getBody().replace("'", '"'))
        responsePost = requests.post(self.__url + request.getUri(), json=body)

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
        body = json.loads(request.getBody().replace("'", '"'))
        responsePatch = requests.patch(self.__url + request.getUri(), json=body)

        response = Response()
        response.setId(request.getId())
        response.setReplyHost(str(request.getReplyHost()))
        response.setReplyPort(int(request.getReplyPort()))
        response.setReplyChannel(str(request.getReplyChannel()))
        response.setVersionProtocol('HTTP/1.0' if responsePatch.raw.version == 10 else 'HTTP/1.1')
        response.setStatusCode(int(responsePatch.status_code))
        response.setStatusMessage(str(responsePatch.reason))
        response.setHeader(str(responsePatch.headers))
        response.setBody(str(responsePatch.text))

        self.__responseProducer.produce(response)

    def delete(self, request):
        responseDelete = requests.delete(self.__url + request.getUri())

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