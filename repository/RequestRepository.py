import sqlite3

from util.Logger import Logger
from model.Request import Request
from model.vo.Protocol import Protocol
from util.StringUtil import StringUtil

class RequestRepository(object):
    def __init__(self):
        self.__connection = None


    def connect(self):
        self.__connection = sqlite3.connect( 'ApiGateway.db' )
        cursor = self.__connection.cursor()
        query = """ CREATE TABLE IF NOT EXISTS request (id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT, replyHost TEXT, replyPort INTEGER, replyChannel TEXT, replyProtocol TEXT); """
        cursor.execute( query )
        cursor.close()

    
    def isConnected(self):
        return self.__connection != None


    def disconnect(self):
        if self.__connection == None: return
        self.__connection.close()
        del( self.__connection )
        self.__connection = None


    def commit(self):
        if self.__connection == None: return
        self.__connection.commit()


    def save(self, request):
        query = """ INSERT INTO request (replyHost, replyPort, replyChannel, replyProtocol) values (?, ?, ?, ?) """
        cursor = self.__connection.cursor()

        replyHost = StringUtil.clean( request.getReplyHost() ) 
        replyPort = StringUtil.clean( request.getReplyPort() )
        replyChannel = StringUtil.clean( request.getReplyChannel() )
        replyProtocol = StringUtil.clean( request.getReplyChannel() )
        parameters = (replyHost, replyPort, replyChannel, replyProtocol)
        cursor.execute(query, parameters)

        requestSaved = Request()
        requestSaved.setId( cursor.lastrowid )
        requestSaved.setReplyHost( request.getReplyHost() )
        requestSaved.setReplyPort( request.getReplyPort() )
        requestSaved.setReplyChannel( request.getReplyChannel() )
        requestSaved.setReplyProtocol( request.getReplyChannel() )
        requestSaved.setOverProtocol( request.getOverProtocol() )
        requestSaved.setMethod( request.getMethod() )
        requestSaved.setUri( request.getUri() )
        requestSaved.setHeader( request.getHeader() )
        requestSaved.setBody( request.getBody() )
        requestSaved.setArriveTime( request.getArriveTime() )
        requestSaved.setDepartureTime( request.getDepartureTime() )
    
        cursor.close()

        return requestSaved


    def findById(self, id):
        query = """ SELECT replyHost, replyPort, replyChannel, replyProtocol FROM request WHERE id = ? """
        parameters = (id,)
        cursor = self.__connection.cursor()
        cursor.execute(query, parameters)

        resultSet = cursor.fetchone()
        request = Request()
        request.setId( id )
        request.setReplyHost( resultSet[0] )
        request.setReplyPort( resultSet[1] )
        request.setReplyChannel( resultSet[2] )
        request.setReplyProtocol( Protocol(resultSet[3][8:]) )

        cursor.close()

        return request
