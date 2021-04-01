import ast
import json

class ObjectUtil:
    
    @staticmethod
    def getDefaultIfNone(input, default):
        if input == None: return default
        return input
    
    @staticmethod
    def isEmpty(input):
        if input == None: return True
        result = len(input) == 0
        return result
    
    @staticmethod
    def getDefaultIfEmpty(input, default):
        if ObjectUtil.isEmpty(input): return default
        return input