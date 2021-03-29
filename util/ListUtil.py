class ListUtil:
    
    @staticmethod
    def append(input, value):
        if input == None: return
        result = input.copy()
        result.append(value)
        return result
    

    @staticmethod
    def extend(input, value):
        if input == None: return
        result = input.copy()
        result.extend(value)
        return result
    
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
    def length(input):
        result = 0 if input == None else len( input )
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
    
    @staticmethod
    def of(input, quantity=1):
        if ( quantity <= 0): return None
        return [ input ] * quantity