# -*- coding: utf-8 -*-
# -------------------------------------------------------------------------------------------------
# dependencies
# -------------------------------------------------------------------------------------------------
from SarBase      import SarBase
from SarParser    import SarParser
from Log          import Log
from re           import compile
from re           import match
from functools    import reduce
from pprint       import pprint
# -------------------------------------------------------------------------------------------------
# Sar Parser
# -------------------------------------------------------------------------------------------------
class SarFilter(SarBase):
# -----------------------------------------------------------------------------
# public
# -----------------------------------------------------------------------------
    # initialization
    # -------------------------------------------------------------------------
    def __init__(self, target=None, filter=None):
        self.__target = target if isinstance(target, list) else [target]
        self.__filter = filter if isinstance(filter, list) else [filter]
    # -------------------------------------------------------------------------
    # process
    # -------------------------------------------------------------------------
    def __call__(self, data):
        print(self.__target)
        # extract target points
        points = reduce(
            lambda a, p: a + list(filter(compile(p).match, data)),
            self.__target, 
            []
        )
        # filter  
        result = {}
        for each in points:
            result[each] = data[each]  
            # find connections 
            find_inputs (data, data[each][ILINK], result)
            find_outputs(data, data[each][OLINK], result)
        # result 
        return result
    # -------------------------------------------------------------------------
    # find input 
    # -------------------------------------------------------------------------
    def find_inputs(data, links, results):
        points = reduce(
            lambda a, p: a + list(filter(compile(p).match, data)),
            self.__filter, 
            []
        )
        filter(compile(p).match, data)
        for each in links:
            if each in data:
                if match(data[each][SarBase.TYPE], self.__filter):
                    pass
    # -------------------------------------------------------------------------
    # find outputs 
    # -------------------------------------------------------------------------
    def find_inputs():
        pass
    
# -----------------------------------------------------------------------------
# private
# -----------------------------------------------------------------------------

# -----------------------------------------------------------------------------
# main
# -----------------------------------------------------------------------------
def main(params):
    # start
    Log.info('Start')
    # xml to python and filter
    SarFilter(params.target, params.filter)(SarParser(params.path)())
    #pprint(SarFilter(params.target, params.filter)(SarParser(params.path)()))
    # finish
    Log.info('Finish')
    return 0
# -------------------------------------------------------------------------------------------------
# end
# -------------------------------------------------------------------------------------------------