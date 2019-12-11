# -*- coding: utf-8 -*-
# -------------------------------------------------------------------------------------------------
# dependencies
# -------------------------------------------------------------------------------------------------
from sar_base     import SarBase
from sar_parser   import SarParser
from log          import Log
from re           import compile, match
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
        for target in self.__target:
            for link in filter(compile(target).match, data):
                if link not in cache:
                    cache[link] = data[link]  
                    # seek connections 
                    self.__seek(SarBase.ILINK, cache[link], data, cache)
                    self.__seek(SarBase.OLINK, cache[link], data, cache)
        return cache
    # -------------------------------------------------------------------------
    # seek
    # -------------------------------------------------------------------------
    def __seek(self, direction, node, data, cache):
        # seek tool
        direction_tool = {
            'ASSEMBLY-SW-CONNECTOR': self.__direction_connector,
        }.get(node[SarBase.TYPE], self.__direction_default)
        # find links
        for link in direction_tool(direction, node):
            if link in cache:
                continue
            if link not in data:
                continue
            for pattern in self.__filter:
                if match(pattern, data[link][SarBase.TYPE]):
                    continue
                cache[link] = data[link]  
                self.__seek(direction, cache[link], data, cache)
    # -------------------------------------------------------------------------
    # directions
    # -------------------------------------------------------------------------
    # default
    # -----------------------------------------------------
    def __direction_default(self, direction, node):
        if direction not in node:
            return
        for link in node[direction]:
            yield link
    # -----------------------------------------------------
    # connector
    # -----------------------------------------------------
    def __direction_connector(self, direction, node):
        for link in node[SarBase.ILINK]:
            yield link
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