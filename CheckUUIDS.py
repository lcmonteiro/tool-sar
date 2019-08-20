
# -*- coding: utf-8 -*-
# -------------------------------------------------------------------------------------------------
# dependencies
# -------------------------------------------------------------------------------------------------
from SarFiles  import SarFiles
from logging   import getLogger as Logger
# -------------------------------------------------------------------------------------------------
# code
# -------------------------------------------------------------------------------------------------
# find key
# ---------------------------------------------------------
def find(key, var):
    if hasattr(var,'items'):
        for k, v in var.items():
            if k == key:
                yield v
            if isinstance(v, dict):
                for result in find(key, v):
                    yield result
            elif isinstance(v, list):
                for d in v:
                    for result in find(key, d):
                        yield result
                    #
                #
            #
        #
    #
#
# ---------------------------------------------------------
# main
# ---------------------------------------------------------
def main(params):
    log = Logger()
    # log
    log.info('Start')
    # xml to python
    data = SarFiles(params.path).process()
    # seek for equal UUIDs
    result = {}
    for f, d in data.items():
        for a in find('UUID', d):
            if a in result:
                log.error("UUID=%s F1=%s F2=%s" % (a, f, result[a]))
            else:
                result[a] = f
            #
        #
    #
    log.info('Finish')
    return 0
# -------------------------------------------------------------------------------------------------
# end
# -------------------------------------------------------------------------------------------------