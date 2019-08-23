class Logger:
    
    @staticmethod
    def debug(message):
        print('[Debug] ' + str(message))

    @staticmethod
    def info(message):
        print('[Info] ' + str(message))

    @staticmethod
    def warn(message):
        print('[Warn] ' + str(message))
    
    @staticmethod
    def error(message):
        print('[Error] ' + str(message))

    @staticmethod
    def fatal(message):
        print('[Fatal] ' + str(message))
    
    @staticmethod
    def off(message):
        print('[Off] ' + str(message))
    
    @staticmethod
    def trace(message):
        print('[TRACE] ' + str(message))

