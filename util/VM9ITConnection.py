import json
import datetime
import requests
import http.client

from util.Logger import Logger
from model.Authentication import Authentication
from model.dao.ConfigurationDAO import ConfigurationDAO

class VM9ITConnection(object):
    def __init__(self):
        self.__properties = ConfigurationDAO('VM9IT')
        self.__address = self.__properties.get('address')
        self.__port = self.__properties.get('port')
        self.__url = 'http://' + self.__address + ':' + self.__port

    def doGet(self, uri):
        header = self.__getHeader()
        responseGet = requests.get(self.__url + uri, headers=header)
        return responseGet

    def doPost(self, uri, body):
        header = self.__getHeader()
        bodyJson = json.loads(body.replace("'", '"'))
        responsePost = requests.post(self.__url + uri, json=bodyJson, headers=header)
        return responsePost

    def doPut(self, uri, body):
        header = self.__getHeader()
        bodyJson = json.loads(body.replace("'", '"'))
        responsePut = requests.put(self.__url + uri, json=bodyJson, headers=header)
        return responsePut

    def doDelete(self, uri):
        header = self.__getHeader()
        responseDelete = requests.delete(self.__url + uri, headers=header)
        return responseDelete

    def __getHeader(self):
        authentication = Authentication.getInstance()
        if ( not authentication.getToken() ) or authentication.hasExpired():
            address = self.__properties.get('address')
            port = self.__properties.get('port')
            grant_type= self.__properties.get('grant_type')
            client_id = self.__properties.get('client_id')
            client_secret = self.__properties.get('client_secret')
            url = address + ':' + port
            payload = 'grant_type=' + grant_type + '&client_id=' + client_id + '&client_secret=' + client_secret
            headers = { 'content-type': 'application/x-www-form-urlencoded' }
            
            conn = http.client.HTTPConnection(url)
            conn.request("POST", "/api/v1/access_token", payload, headers)
            response = json.loads(str(conn.getresponse().read().decode("utf-8")))

            authentication.setLast(datetime.datetime.now())
            authentication.setToken(str(response['access_token']))
            authentication.setType(str(response['token_type']))
            authentication.setExpires(int(response['expires_in']))

        header = dict()
        header['Authorization'] = authentication.getType() + ' ' + authentication.getToken()
        return header