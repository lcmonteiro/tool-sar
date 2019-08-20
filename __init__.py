# -*- coding: utf-8 -*-
#
from SarFiles     import SarFiles
from SarSearch    import SarSearch
from SarParser    import SarParser

from pprint       import pprint
#
if __name__ == '__main__':    
    #
    data = SarParser('data').process()
    #
    types = {}
    for k, v in data.items():
        try :
            if v['$'] in types:
                types[v['$']] += [k]
            else :
                types[v['$']] = [k] 
        except:
            pass
    #
    pprint(list(types.keys()))
    #pprint(dict(list(data.items())[0:10]))
    #
    #print(data)
    #print(len(data))
    #
#

#
#-----------------------------------------------------------------------------------------------------------------------
# translate
#-----------------------------------------------------------------------------------------------------------------------
#
def normalize(param):
        result = {}
        #
        if param.file:
                result['file'] = param.file
        #
        if param.size:
                result['size'] = param.size
        #
        if param.box:
                result['box'] = dict([(i[0], i[1]) for i in param.box]) 
        #
        if param.clear:
                result['clear'] = param.clear
        #
        if param.keep:
                result['keep'] = param.keep
        #
        return result
#
#-----------------------------------------------------------------------------------------------------------------------
# main
#-----------------------------------------------------------------------------------------------------------------------
def main(param):
        print normalize(param)
        #
        # select command
        #
        return {
                'create': create, 
                'encode': encode,
                'decode': decode,
                "delete": delete
        }[param.cmd](normalize(param))
#   
#-----------------------------------------------------------------------------------------------------------------------
# entry point
#-----------------------------------------------------------------------------------------------------------------------
from sys import exit
#
if __name__ == '__main__':
    # -------------------- read args -----------------------------------------------
    params = parseinput('File Share', '1.0.0', [{
                        'opt': ['cmd'], 'settings': {
                        'help': 'commands',
                        'choices': ['create', 'encode', 'decode', 'destroy']
                }}, {
                        'opt': ['file'], 'settings': {
                        'help': 'file path',
                        'nargs':'?',
                        'metavar':'FILE'
                }}, {
                        'opt': ['-s', '--size'], 'settings': {
                        'help': 'file size',
                        'nargs':1,
                        'default': None
                }}, {
                        'opt': ['-b', '--box'], 'settings': {
                        'nargs':2,
                        'action':'append',
                        'metavar':('URI', 'SIZE'),
                        'help': 'box parameters (uri and size)'
                }}, {
                        'opt': ['-p', '--password'], 'settings': {
                        'help': 'request password',
                        'action': 'store_true'
                }}, {
                        'opt': ['-c', '--clear'], 'settings': {
                        'help': 'clear files',
                        'action': 'store_true'
                }}, {
                        'opt': ['-k', '--keep'], 'settings': {
                        'help': 'clear files',
                        'action': 'store_true'
                }}
        ])
    # --------------- main ---------------------------------------------------------
    try:
        res = main(params)
    except Exception as inst:
        print 'fshare:: error:', inst 
        exit(-1)
    #
    exit(res)
#-----------------------------------------------------------------------------------------------------------------------
