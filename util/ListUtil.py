class ListUtil:
    
    @staticmethod
    def getNoneAsEmpty(input):
        result = [] if input == None else input
        return result

    
    @staticmethod
    def getEmptyAsNone(input):
        result = None if input == [] else input
        return result
    
    
    @staticmethod
    def isEmpty(input):
        if input == None : return True
        result = input == []
        return result
    
    
    @staticmethod
    def toTuple(input):
        if input == None: return None
        return tuple( input )

    
    @staticmethod
    def toDict(input):
        if input == None: return None
        return dict( input )

    
    @staticmethod
    def toString(input):
        if input == None: return ''
        return str( input )