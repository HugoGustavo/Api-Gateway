import json

class JsonUtil:
    
    @staticmethod
    def getNoneAsEmpty(input):
        result = dict() if input == None else input
        return result

    
    @staticmethod
    def toString(input):
        input = JsonUtil.getNoneAsEmpty( input )
        return json.dumps( input )
