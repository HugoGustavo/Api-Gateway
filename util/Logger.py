import datetime

class Logger:
    
    @staticmethod
    def debug(message):
        timestamp = str( datetime.datetime.now() )
        print(timestamp + ' [DEBUG] ' + str( message ))

    
    @staticmethod
    def info(message):
        timestamp = str( datetime.datetime.now() )
        print(timestamp + ' [INFO] ' + str( message ))

    
    @staticmethod
    def warn(message):
        timestamp = str( datetime.datetime.now() )
        print(timestamp + ' [WARN] ' + str( message ))
    
    
    @staticmethod
    def error(message):
        timestamp = str( datetime.datetime.now() )
        print(timestamp + ' [ERROR] ' + str( message ))

    
    @staticmethod
    def fatal(message):
        timestamp = str( datetime.datetime.now() )
        print(timestamp + ' [FATAL] ' + str( message ))
    
    
    @staticmethod
    def off(message):
        timestamp = str( datetime.datetime.now() )
        print(timestamp + ' [OFF] ' + str( message ))
    
    
    @staticmethod
    def trace(message):
        timestamp = str( datetime.datetime.now() )
        print(timestamp + ' [TRACE] ' + str( message ))

