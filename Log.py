# -*- coding: utf-8 -*-
#-----------------------------------------------------------------------------------------------------------------------
# dependencies
#-----------------------------------------------------------------------------------------------------------------------
from colorama  import Fore, Back, Style
from time      import gmtime
from time      import strftime
#-----------------------------------------------------------------------------------------------------------------------
# log function
#-----------------------------------------------------------------------------------------------------------------------
class Log:
    __debugLevel = 0

    def __init__(self, level):
        Log.__debugLevel = level

#static
    @staticmethod
    def debug(data):
        if Log.__debugLevel < 1:
            print(Fore.GREEN + "[ " + strftime("%Y-%m-%d %H:%M:%S", gmtime()) + " ]" + " [ DEBUG  ] " + " [ " + x + " ] ")
        #
    #
    @staticmethod
    def info(data):
        if Log.__debugLevel < 2:
            print(Fore.GREEN + "[ " + strftime("%Y-%m-%d %H:%M:%S", gmtime()) + " ]" + " [ INFO  ] " + " [ " + x + " ] ")
        #
    #
    @staticmethod
    def warning(data):
        if Log.__debugLevel < 3:
            print(Fore.YELLOW + "[ " + strftime("%Y-%m-%d %H:%M:%S", gmtime()) + " ]" + " [ WARNING ] " + " [ " + x + " ] ")
        #
    #
    #
    @staticmethod
    def error(data):
        if Log.__debugLevel < 3:
            print(Fore.RED + "[ " + strftime("%Y-%m-%d %H:%M:%S", gmtime()) + " ]" + " [ WARNING ] " + " [ " + x + " ] ")
        #
    #
#