import time
import requests

from util.Logger import Logger
from model.Request import Request
from model.Response import Response
from util.StringUtil import StringUtil
from producer.ResponseProducer import ResponseProducer
from model.dao.ConfigurationDAO import ConfigurationDAO

class FiwareOrionService(object):
    def __init__(self, responseProducer):
        self.__properties = ConfigurationDAO( 'FiwareOrionBroker' )
        self.__address = self.__properties.get( 'address' )
        self.__port = self.__properties.get( 'port' )
        self.__url = 'http://' + self.__address + ':' + self.__port
        self.__responseProducer = responseProducer


    def read(self, request):
        responseGet = requests.get( self.__url + request.getUri() )

        response = Response()
        response.setId(request.getId())
        response.setReplyHost( StringUtil.clean(request.getReplyHost()) )
        response.setReplyPort( StringUtil.toInt(request.getReplyPort()) )
        response.setReplyChannel( StringUtil.clean(request.getReplyChannel()) )
        response.setVersionProtocol( 'HTTP/1.0' if responseGet.raw.version == 10 else 'HTTP/1.1' )
        response.setStatusCode( StringUtil.toInt(responseGet.status_code) )
        response.setStatusMessage( StringUtil.clean(responseGet.reason) )
        response.setHeader( StringUtil.clean(responseGet.headers) )
        response.setBody( StringUtil.clean(responseGet.text) )

        self.__responseProducer.produce( response ) 


    def create(self, request):
        body = StringUtil.toJson( request.getBody() )
        responsePost = requests.post(self.__url + request.getUri(), json=body)

        response = Response()
        response.setId( request.getId() )
        response.setReplyHost( StringUtil.clean(request.getReplyHost()) )
        response.setReplyPort( StringUtil.toInt(request.getReplyPort()) )
        response.setReplyChannel( StringUtil.clean(request.getReplyChannel()) )
        response.setVersionProtocol( 'HTTP/1.0' if responsePost.raw.version == 10 else 'HTTP/1.1' )
        response.setStatusCode( StringUtil.toInt(responsePost.status_code) )
        response.setStatusMessage( StringUtil.clean(responsePost.reason) )
        response.setHeader( StringUtil.clean(responsePost.headers) )
        response.setBody( StringUtil.clean(responsePost.text) )

        self.__responseProducer.produce( response )


    def update(self, request):
        body = StringUtil.toJson( request.getBody().replace("'", '"' ) )
        responsePatch = requests.patch(self.__url + request.getUri(), json=body)

        response = Response()
        response.setId( request.getId() )
        response.setReplyHost( StringUtil.clean(request.getReplyHost()) )
        response.setReplyPort( StringUtil.toInt(request.getReplyPort()) )
        response.setReplyChannel( StringUtil.clean(request.getReplyChannel()) )
        response.setVersionProtocol( 'HTTP/1.0' if responsePatch.raw.version == 10 else 'HTTP/1.1' )
        response.setStatusCode( StringUtil.toInt(responsePatch.status_code) )
        response.setStatusMessage( StringUtil.clean(responsePatch.reason) )
        response.setHeader( StringUtil.clean(responsePatch.headers) )
        response.setBody( StringUtil.clean(responsePatch.text) )

        self.__responseProducer.produce( response )


    def delete(self, request):
        responseDelete = requests.delete(self.__url + request.getUri())

        response = Response()
        response.setId( request.getId() )
        response.setReplyHost( StringUtil.clean(request.getReplyHost()) )
        response.setReplyPort( StringUtil.toInt(request.getReplyPort()) )
        response.setReplyChannel( StringUtil.clean(request.getReplyChannel()) )
        response.setVersionProtocol( 'HTTP/1.0' if responseDelete.raw.version == 10 else 'HTTP/1.1' )
        response.setStatusCode( StringUtil.toInt(responseDelete.status_code) )
        response.setStatusMessage( StringUtil.clean(responseDelete.reason) )
        response.setHeader( StringUtil.clean(responseDelete.headers) )
        response.setBody( StringUtil.clean(responseDelete.text) )

        self.__responseProducer.produce( response ) 