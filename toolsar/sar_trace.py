# -*- coding: utf-8 -*-
# -------------------------------------------------------------------------------------------------
# dependencies
# -------------------------------------------------------------------------------------------------
from toolsar.sar_base   import SarBase
from toolsar.sar_parser import SarParser
from toolsar.log        import Log
from re                 import compile, match
from functools          import reduce
from pprint             import pprint

# -------------------------------------------------------------------------------------------------
# Trace
# -------------------------------------------------------------------------------------------------
def load(path, cache):
    from pickle import load, dump
    parser = SarParser(path)
    data   = {}
    try:
        with open(cache, 'rb') as f:
            data = load(f)
    except FileNotFoundError:
        data = parser()
        with open(cache, 'wb') as f:
            dump(data, f)
    return data

def trace(pattern, doc):
    pass
# -----------------------------------------------------------------------------
# main
# -----------------------------------------------------------------------------
import yaml   as yl
def main(params):
    import networkx as nx
    import matplotlib.pyplot as plt
    G = nx.Graph()
    G.add_edge("NA12878", "NA12892", weight=2)
    G.add_edge("NA12878", "NA12891", weight=7)
    G.add_edge("NA12892", "NA12891", weight=4)

    G.add_node("NA12878", relationship="child")
    G.add_node("NA12892", relationship="mother")
    G.add_node("NA12891", relationship="father")
    

    nx.draw_shell(G)
    plt.show()



    # start
    Log.info('Start Trace')
    # load data
    data = load(params.path, 'cache.pickle')

    PATTERN = '.*DispDrasyLng.*'

    from re import match

    data = dict(filter(lambda d: match(PATTERN, d[0]), data.items())) 

    for k, v in data.items():
        print('\n {:<100} : {:<100}'.format(k, v['$']))
        for kk, vv in v.get('<-', {}).items():
            print('\t {:<100} : {:<100}'.format(kk, vv))
        for kk, vv in v.get('->', {}).items():
            print('\t {:<100} : {:<100}'.format(kk, vv))
    
    # finish
    Log.info('Finish Trace')
    return 0
# -------------------------------------------------------------------------------------------------
# end
# -------------------------------------------------------------------------------------------------