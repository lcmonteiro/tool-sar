# -*- coding: utf-8 -*-
# -------------------------------------------------------------------------------------------------
# dependencies
# -------------------------------------------------------------------------------------------------
from XmlTransform  import XmlTransform
from SarTransform  import SarTransform
from TreeTransform import TreeTransform
from file_search    import file_search
from SarBase       import SarBase
from Log           import Log
# -------------------------------------------------------------------------------------------------
# Sar Parser
# -------------------------------------------------------------------------------------------------
class SarParser(SarBase):
# -----------------------------------------------------------------------------
# public
# -----------------------------------------------------------------------------
    # initialization
    # -------------------------------------------------------------------------
    def __init__(self, path):
        self.__path = path
    # ------------------------------------------------------------------------- 
    # process
    # -------------------------------------------------------------------------
    def __call__(self):
        result = {}
        # find all arxml
        for f in self.__findFiles():
            # prase and merge 
            try :
                result = self.__mergeData(result, self.__parseFile(f))
            except Exception as e:
                Log.warning("file=%s exception=%s" %(f, str(e)))
        # link data 
        result = self.__linkData(result)
        return result
    #
# -----------------------------------------------------------------------------
# private
# -----------------------------------------------------------------------------
    def __parseFile(self, path):
        #
        result = {}
        with open(path) as fd:
            # xml to var
            result = XmlTransform.toVar(fd.read())
            # var to tree
            result = TreeTransform('SHORT-NAME').run(result)
            # var to sar
            result = SarTransform.prepare(result)
        #
        return result
    #
    def __mergeData(self, data, doc):
        #
        result = SarTransform.insert(data, doc)
        #
        return result
    #
    def __linkData(self, data):
        return SarTransform.link(data)
    #
    def __findFiles(self):
        if isinstance(self.__path, list):
            return self.__path
        else:
            return file_search.find(self.__path, '.*arxml$')
        #
    #
#
# -----------------------------------------------------------------------------
# main
# -----------------------------------------------------------------------------
def main(params):
    from yaml import dump
    # start
    Log.info('Start')
    # xml to python
    data = SarParser(params.path)()
    # print 
    print(dump(data))
    # finish
    Log.info('Finish')
    return 0
# -------------------------------------------------------------------------------------------------
# end
# -------------------------------------------------------------------------------------------------