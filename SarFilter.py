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
    def __call__(self, data, cache={}):
        # ---------------------------------------------------------------------
        # find
        # ---------------------------------------------------------------------
        def find(direction, node, data, cache):
            if direction not in node:
                return
            for link in node[direction]:
                if link in cache:
                    continue
                if link not in data:
                    continue
                for pattern in self.__filter:
                    if match(pattern, data[link][SarBase.TYPE]):
                        continue
                    cache[link] = data[link]
                    if cache[link][SarBase.TYPE] == 'ASSEMBLY-SW-CONNECTOR':
                        print(link)
                        find(SarBase.OLINK, cache[link], data, cache)    
                    find(direction, cache[link], data, cache)
        # ---------------------------------------------------------------------
        # execute
        # ---------------------------------------------------------------------
        for target in self.__target:
            for link in filter(compile(target).match, data):
                if link not in cache:
                    cache[link] = data[link]  
                    # find connections 
                    find(SarBase.ILINK, cache[link], data, cache)
                    find(SarBase.OLINK, cache[link], data, cache)
        return cache
# -----------------------------------------------------------------------------
# main
# -----------------------------------------------------------------------------
from yaml import dump
def main(params):
    # start
    Log.info('Start')
    # xml to python and filter
    #SarFilter(params.target, params.filter)(SarParser(params.path)())
    print(dump(SarFilter(params.target, params.filter)(SarParser(params.path)())))
    # finish
    Log.info('Finish')
    return 0
# -------------------------------------------------------------------------------------------------
# end
# -------------------------------------------------------------------------------------------------