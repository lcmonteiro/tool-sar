# -*- coding: utf-8 -*-
# -------------------------------------------------------------------------------------------------
# dependencies
# -------------------------------------------------------------------------------------------------
from toolsar.var_search import VarSearch
from toolsar.sar_base   import SarBase
from re                 import match
# -------------------------------------------------------------------------------------------------
# Sar Search
# -------------------------------------------------------------------------------------------------
class SarSearch(SarBase):
#--------------------------------------------------------------------------------------------------
# public
#--------------------------------------------------------------------------------------------------
    # Filter 
    #--------------------------------------------------------------------------
    @staticmethod
    def filter(data, pattern, overlap = 10):
        result = {}
        keys   = []
        #--------------------------------------------------
        # update - check cyclic references
        #--------------------------------------------------
        def __update(key, data):
            if key in result:
                keys.append(key)
                if len(keys) > overlap:
                    raise Exception(keys)
                #
            else:
                keys.clear()
                result[key] = data
            #
        #--------------------------------------------------
        # vertical search
        #--------------------------------------------------
        def __vertical(doc, tagh, tagv, patt):
            try:
                for k in doc[tagv]:
                    try:
                        d = data[k]
                        for p in SarSearch.__find(patt.get(tagv, {".*":{}}), k, d): 
                            # update
                            __update(k, d)
                            # horizontal
                            __horizontal(d, tagh, tagv, p)
                            # vertical
                            __vertical(d, tagh, tagv, p)
                    except:
                        pass
                    #
                #
            except:
                pass
            #
        #--------------------------------------------------
        # horizontal Search
        #--------------------------------------------------
        def __horizontal(doc, tagh, tagv, patt):
            try:
                for k in doc[tagh]:
                    try:
                        d = data[k]
                        for p in SarSearch.__find(patt.get(tagh, {".*":{}}), k, d): 
                            # update
                            __update(k, d)
                            # vertical
                            __vertical(d, tagh, tagv, p)
                            # horizontal
                            __horizontal(d, tagh, tagv, p)
                        #
                    except:
                        pass
                    #
                #
            except:
                pass
        #------------------------------------------------
        # main search
        #------------------------------------------------
        for k, d in data.items():
            for p in SarSearch.__find(pattern, k, d):
                try:
                    # update
                    __update(k, d)
                    for h, v in [(SarBase.PARENT, SarBase.ILINK), (SarBase.CHILDREN, SarBase.OLINK)]:
                        # vertical
                        __vertical(d, h, v, p)
                        # horizontal
                        __horizontal(d, h, v, p)
                    #
                except:
                    pass
                #
            #
        #
        return result
    #--------------------------------------------------------------------------
    # Count 
    #--------------------------------------------------------------------------
    @staticmethod
    def count(data):
        result = {}
        for d in data:
            try:
                result[data[d][SarBase.TYPE]] += 1
            except:
                try:
                    result[data[d][SarBase.TYPE]] = 1
                except:
                    result[''] = 1
                #
            #
        #
        #
        c = [[v,k] for k, v in result.items()]
        c.sort(reverse=True)
        print(c)
        return result
    #
#--------------------------------------------------------------------------------------------------
# private
#--------------------------------------------------------------------------------------------------
    # find pattern
    #--------------------------------------------------------------------------
    def __find(pattern, key, doc):
        if isinstance(pattern, str):
            pattern = dict([(pattern, {})])
        elif isinstance(pattern, list):
            pattern = dict([(p, {})for p in pattern])
        #-----------------------------------
        # match function
        # ----------------------------------
        def __match(p, k, d):
            try:
                if not match(p, k):
                    return False
                if SarBase.TYPE in pattern[p]:
                    if not VarSearch.contains(pattern[p][SarBase.TYPE], doc[SarBase.TYPE]):
                        return False
                if SarBase.PROPERTY in pattern[p]:
                    if not VarSearch.contains(pattern[p][SarBase.TYPE], doc[SarBase.PROPERTY]):
                        return False
                    #
                return True
            except:
                return False
            #
        #-----------------------------------
        # main
        # ----------------------------------
        return [pattern[p] for p in pattern if __match(p, key, doc)]
    #
#----------------------------------------------------------------------------------------------------
# testes
#----------------------------------------------------------------------------------------------------
if __name__ == '__main__':
    from pprint import pprint
    data = {
        "/a": {
            "$" : "ROOT"
         },
         "/a/a": {
             "$": "BSW-MODULE-ENTRY",
             ".." : {
                 "/" : "ROOT"
             },
             "<>" : {
                 "/a/a/a": "BEHAVIOR"
             },
             "<-" : {
                 "/a/b": "BSW-CALLED-ENTITY"
             },
             "->" : {
                 "/a/c" : "IMPLEMENTATION-DATA-TYPE"
             },
             "@": {
              "IMPLEMENTED-ENTRY-REF": {
                "#": "/AUTOSAR_Rte/BswModuleEntrys/Rte_Stop",
                "@": {
                  "DEST": "BSW-MODULE-ENTRY"
                }
              },
              "MINIMUM-START-INTERVAL": "0"
            }
         },
         "/a/b": {
             "$" : "BSW-MODULE-ENTRY",
             ".." : {
                 "/" : "ROOT"
             },
             "<>" : {
                 "/a/a/a": "BEHAVIOR"
             },
             "->" : {
                 "/a/c" : "IMPLEMENTATION-DATA-TYPE"
             }
         },
         "/a/c": {
             "$" : "BSW-MODULE-ENTRY",
             ".." : {
                 "/" : "ROOT"
             },
             "<>" : {
                 "/a/c/a": "BEHAVIOR"
             },
             "<-" : {
                 "/a/a": "BSW-CALLED-ENTITY"
             },
             "->" : {
                 "/a" : "IMPLEMENTATION-DATA-TYPE"
             }
         },
         "/a/b/a": {
             "$" : "BSW-MODULE-ENTRY",
             ".." : {
                 "/" : "ROOT"
             },
             "<>" : {
                 "/a/c/a": "BEHAVIOR"
             },
             "<-" : {
                 "/a/a": "BSW-CALLED-ENTITY"
             }
         },
         "/a/a/a": {
             "$" : "BSW-MODULE-ENTRY",
             ".." : {
                 "/" : "ROOT"
             },
             "<>" : {
                 "/a/a/a": "BEHAVIOR"
             },
             "<-" : {
                 "/a/a": "BSW-CALLED-ENTITY"
             }
         } 
    }
    #
    # Test1
    #
    pprint(SarSearch.filter(data, {
        "/a/b$": {
            "$" : ".",
            "<>":{
            }
        }
    }))
    #
    # Test2
    #
#
