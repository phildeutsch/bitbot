#!/usr/bin/python3

import sys
sys.path.append('./source')
sys.path.append('./api')

import apiKraken
from bbClasses import *
from bbSettings import *
from bbFunctions import *
from bbKeysMonitor import *

import datetime
import time
import re

def main():
    testFlag  = 1
    
    t         = trader(logFileName, walkUp, walkDown, midDistance, tradeBuffer, 
                   priceWindow, tradeFactor)
    p         = portfolio(1,0)
    m         = marketData('Null', 0, 0, priceWindow)
    krakenAPI = apiKraken.API(keyKraken, secKraken)

    while True:
        mainLoop(m, p, t, krakenAPI, testFlag)

        if testFlag == 1:
            break

def mainLoop(m, p, t, api, testFlag):
    api.getBalance(m, p, t)
    api.getPrices(m, t.minTrade)
    
    t.stopLoss(m, stopLossLimit, overrideFileName)
    t.updateBounds(m)
    t.calcBaseWeight(m)
    t.calcMomentum(momFactor, m)
    t.checkOverride(overrideFileName)
    
    t.calcCoinsToTrade(m, p)
    t.checkTradeSize(m, p, tradeFactor)
    
    if t.suspend != 1 and testFlag != 1:
        cancelOrders(krakenAPI, t)
        placeOrder(krakenAPI, m, t)

    if testFlag == 1:
        printTermLine(m, p, t)
    else:
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
