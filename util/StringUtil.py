import ast
import json

class StringUtil:
    
    @staticmethod
    def length(input):
        result = 0 if input == None else len( input )
        return result
  
    
    @staticmethod
    def isEmpty(input):
        if input == None: return True
        return '' == StringUtil.clean( input )
    
    
    @staticmethod
    def substring(input, start, end):
        if input == None: return None
        return str(input)[start:end]
    
    
    @staticmethod
    def split(input, separator=" "):
        if input == None: return None
        return str(input).split( separator )

    
    @staticmethod
    def isNotEmpty(input):
        return not StringUtil.isEmpty( input )

    
    @staticmethod
    def getNoneAsEmpty(input):
        result = '' if input == None else input
        return result
        
    
    @staticmethod
    def getEmptyAsNone(input):
        if input == None : return None
        result = None if StringUtil.isEmpty( input ) else input
        return result

    @staticmethod
    def clean(input):
        if input == None : return ''
        return str(input).strip()
    
    
    @staticmethod
    def toInt(input):
        if input == None : return None
        result = StringUtil.clean( input )
        return int(result)

    
    @staticmethod
    def toFloat(input):
        if input == None : return None
        result = StringUtil.clean( input )
        return float(result)
    
    
    @staticmethod
    def toDict(input):
        if input == None : return None
        result = StringUtil.clean( input )
        return ast.literal_eval( result )
    
    
    @staticmethod
    def toJson(input):
        if input == None : return None
        result = StringUtil.clean( input )
        return json.loads( input )
