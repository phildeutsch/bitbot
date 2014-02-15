#!/usr/bin/python3

import sys
sys.path.append('./source')
sys.path.append('./api')

import apiKraken
import apiBacktest
from bbClasses import *
from bbSettings import *
from bbFunctions import *
from bbKeysTrader import *

import datetime
import getopt
import time
import re

def main(argv=None):
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

    p         = portfolio(100,0)
    m         = marketData('Null', 0, 0, priceWindow)
    if btFlag == 0:
        API = apiKraken.API(keyKraken, secKraken)
        t   = trader(logFileName, walkUp, walkDown, midDistance, tradeBuffer, 
                           priceWindow, tradeFactor)
    else:
        API = apiBacktest.API(logFileName)
        with open(logFileNameBT, 'w') as logBT:
            logBT.write('Time,Bid,Ask,EUR,BTC,Trade,minPrice,maxPrice\n')
        t   = trader(logFileNameBT, walkUp, walkDown, midDistance, tradeBuffer, 
                       priceWindow, tradeFactor)

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
        t.stopLoss(m, p, t, stopLossLimit, overrideFileName)
    t.updateBounds(m)
    t.calcBaseWeight(m)
    t.calcMomentum(momFactor, m)
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
            cancelOrders(api, t)
            placeOrder(api, m, t)

        printTermLine(m, p, t)
        printStatus(m, p, t, statusFileName, freezeFileName)
        printLogLine(m, p, t, logFileName)
        if abs(t.coinsToTrade) > 0:
            printLogLine(m, p, t, txFileName)

        timeNow = datetime.datetime.now()
        delay   = (10 - (timeNow.minute)%10) * 60 - timeNow.second
        time.sleep(delay)

if __name__ == "__main__":
    main()
