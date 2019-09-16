import json
import datetime
import http.client

from util.Logger import Logger
from model.Authentication import Authentication
from model.dao.ConfigurationDAO import ConfigurationDAO

class VM9ITConnection(object):
    def __init__(self):
        self.__properties = ConfigurationDAO('VM9IT')

    def getHeader(self):
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
        Logger.info('Authorization: ' + str(header['Authorization']))
        return header