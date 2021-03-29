import ast
import json

class ObjectUtil:
    
    @staticmethod
    def getDefaultIfNone(input, default):
        if input == None: return default
        return input