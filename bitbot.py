#!/usr/bin/python3

import sys
sys.path.append('./source')
sys.path.append('./api')

import apiKraken
import apiBacktest
from bbSettings import *
from bbClasses import *
from bbFunctions import *
from bbKeysTrader import *

import datetime
import getopt
import time
import re

def main(argv=None):
    testFlag, btFlag = argParser(argv)

    # Use data from exchange
    if btFlag == 0:
        API = apiKraken.API(keyKraken, secKraken)
        t   = trader(logFileName, walkUp, walkDown, priceWindow, tradeFactor, 
                     momFactor, backupFund, allinLimit, stopLossLimit)
    # Use data from logfile
    else:
        API = apiBacktest.API(logFileName)
        with open(logFileNameBT, 'w') as logBT:
            logBT.write('Time,Bid,Ask,EUR,BTC,Trade,minPrice,maxPrice\n')
        t   = trader(logFileNameBT, walkUp, walkDown, priceWindow, tradeFactor, 
                     momFactor, backupFund, allinLimit, stopLossLimit)

    p         = portfolio(100,0)
    m         = marketData('Null', 500, 500, priceWindow)

    while True:
        mainLoop(m, p, t, API, testFlag, btFlag)

        if testFlag == 1:
            break
        if btFlag == 1 and API.line == file_len(logFileName):
            break

def mainLoop(m, p, t, api, testFlag, btFlag):
    api.getBalance(m, p, t)
    api.getPrices(m, t.minTrade)
    
    if btFlag != 1:
        t.stopLoss(m, p, overrideFileName)
    t.updateBounds(m)
    t.calcBaseWeight(m)
    t.calcMomentum(m)
    t.checkAllin(m, btFlag)
    t.checkOverride(overrideFileName)
    
    t.calcCoinsToTrade(m, p)
    t.checkTradeSize(m, p, tradeFactor)
 
    if testFlag == 1:
        printTermLine(m, p, t)
    elif btFlag == 1:
        printLogLine(m, p, t, logFileNameBT, bounds = 1)
        if abs(t.coinsToTrade) > 0:
            printTermLine(m, p, t)

    else:
        if t.suspend != 1:
            api.cancelOrders(t)
            api.placeOrder(m, t)

        printTermLine(m, p, t)
        printStatus(m, p, t, statusFileName, freezeFileName)
        printLogLine(m, p, t, logFileName)
        drawplot(m, t, plotFileName)
        if abs(t.coinsToTrade) > 0:
            printLogLine(m, p, t, txFileName)

        timeNow = datetime.datetime.now()
        delay   = (10 - (timeNow.minute)%10) * 60 - timeNow.second
        time.sleep(delay)

def argParser(argv):
    testFlag = 0
    btFlag   = 0

    if argv is None:
        argv = sys.argv[1:]
    else:
        argv = argv.split()
    opts, args = getopt.getopt(argv, 'bt')
    for o, a in opts:
        if o == '-b':
            btFlag = 1
        elif o == '-t':
            testFlag = 1
    
    return testFlag, btFlag

if __name__ == "__main__":
    main()
