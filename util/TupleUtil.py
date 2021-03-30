import ast
import json

from util.StringUtil import StringUtil
from util.Logger import Logger

class TupleUtil:

    @staticmethod
    def length(input):
        if input == None: return 0
        result = len(input)
        return result
    
    
    @staticmethod
    def isEmpty(input):
        if input == None: return True
        result = TupleUtil.length(input) == 0
        return result
  