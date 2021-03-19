import json

class Request(object):
    def __init__(self, id=None, replyHost=None, replyPort=None, replyChannel=None, method=None, uri=None, header=None, body=None, arriveTime=None, departureTime=None):
        self.id = id
        self.replyHost = replyHost
        self.replyPort = replyPort
        self.replyChannel = replyChannel
        self.method = method
        self.uri = uri
        self.header = header
        self.body = body
        self.arriveTime = arriveTime
        self.departureTime = departureTime


    def getId(self):
        return self.id


    def setId(self, id):
        self.id = id


    def getReplyHost(self):
        return self.replyHost


    def setReplyHost(self, replyHost):
        self.replyHost = replyHost


    def getReplyPort(self):
        return self.replyPort


    def setReplyPort(self, replyPort):
        self.replyPort = replyPort


    def getReplyChannel(self):
        return self.replyChannel


    def setReplyChannel(self, replyChannel):
        self.replyChannel = replyChannel


    def getMethod(self):
        return self.method


    def setMethod(self, method):
        self.method = method


    def getUri(self):
        return self.uri


    def setUri(self, uri):
        self.uri = uri


    def getHeader(self):
        return self.header


    def setHeader(self, header):
        self.header = header


    def getBody(self):
        return self.body


    def setBody(self, body):
        self.body = body

    
    def getArriveTime(self):
        return self.arriveTime
    
    
    def setArriveTime(self, arriveTime):
        self.arriveTime = arriveTime
    

    def getDepartureTime(self):
        return self.departureTime

    
    def setDepartureTime(self, departureTime):
        self.departureTime = departureTime
    
    def __str__(self):
        return str( json.dumps(self.__dict__) )