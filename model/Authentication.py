import datetime

class Authentication(object):
    __instance = None

    def __init__(self):
        if Authentication.__instance != None:
            raise Exception('This class is a singleton')

        self.__token = None
        self.__type = None
        self.__last = None
        self.__expires = None

    @staticmethod
    def getInstance():
        if Authentication.__instance == None:
            Authentication.__instance = Authentication()
        return Authentication.__instance

    def getToken(self):
        return self.__token

    def setToken(self, token):
        self.__token = token
    
    def getType(self):
        return self.__type

    def setType(self, type):
        self.__type = type
    
    def getLast(self):
        return self.__last

    def setLast(self, last):
        self.__last = last
    
    def getExpires(self):
        return self.__expires

    def setExpires(self, expires):
        self.__expires = expires

    def hasExpired(self):
        expiredOn = self.__last + datetime.timedelta(seconds=self.__expires)
        return datetime.datetime.now() >= expiredOn