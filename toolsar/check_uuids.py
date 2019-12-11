
# -*- coding: utf-8 -*-
# -------------------------------------------------------------------------------------------------
# dependencies
# -------------------------------------------------------------------------------------------------
from sar_files  import SarFiles
from log        import Log
# -------------------------------------------------------------------------------------------------
# code
# -------------------------------------------------------------------------------------------------
# find key
# -----------------------------------------------------------------------------
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
# -----------------------------------------------------------------------------
# main
# -----------------------------------------------------------------------------
def main(params):
    # log
    Log.info('Start')
    # xml to python
    data = SarFiles(params.path)()
    # seek for equal UUIDs
    result = {}
    for f, d in data.items():
        for a in find('UUID', d):
            if a in result:
                Log.error("UUID=%s F1=%s F2=%s" % (a, f, result[a]))
            else:
                result[a] = f
            #
        #
    #
    Log.info('Finish')
    return 0
# -------------------------------------------------------------------------------------------------
# end
# -------------------------------------------------------------------------------------------------