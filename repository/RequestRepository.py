import sqlite3
from model.Request import Request

class RequestRepository(object):
    def __init__(self, connection):
        self.__connection = connection
        cursor = self.__connection.cursor()
        query = """ CREATE TABLE IF NOT EXISTS request (id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT, replyHost TEXT, replyPort INTEGER, replyChannel TEXT ); """
        cursor.execute(query)
        cursor.close()


    def save(self, request):
        query = """ INSERT INTO request (replyHost, replyPort, replyChannel) values (?, ?, ?) """
        cursor = self.__connection.cursor()

        replyHost = str(request.getReplyHost())
        replyPort = str(request.getReplyPort())
        replyChannel = str(request.getReplyChannel())
        parameters = (replyHost, replyPort, replyChannel)
        cursor.execute(query, parameters)

        requestSaved = Request()
        requestSaved.setId(cursor.lastrowid)
        requestSaved.setReplyHost(request.getReplyHost())
        requestSaved.setReplyPort(request.getReplyPort())
        requestSaved.setReplyChannel(request.getReplyChannel())
        requestSaved.setMethod(request.getMethod())
        requestSaved.setUri(request.getUri())
        requestSaved.setHeader(request.getHeader())
        requestSaved.setBody(request.getBody())
    
        cursor.close()

        return requestSaved
    
    def findById(self, id):
        query = """ SELECT replyHost, replyPort, replyChannel FROM request WHERE id = ? """
        parameters = (id,)
        cursor = self.__connection.cursor()
        cursor.execute(query, parameters)

        resultSet = cursor.fetchone()
        request = Request()
        request.setId(id)
        request.setReplyHost(resultSet[0])
        request.setReplyPort(resultSet[1])
        request.setReplyChannel(resultSet[2])

        cursor.close()

        return request