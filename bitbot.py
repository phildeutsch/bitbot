#!/usr/bin/python3

import sys
sys.path.append('./source')
sys.path.append('./api')

import apiKraken
from bbClasses import *
from bbSettings import *
from bbFunctions import *
from bbKeysTrader import *

import datetime
import time
import re

t         = trader(logFileName, walkUp, walkDown, midDistance, tradeBuffer, 
                   priceWindow)
p         = portfolio(1,0)
m         = marketData('Null', 0, 0, priceWindow)
krakenAPI = apiKraken.API(key, secret)

while True:
    m, p, t = getData(krakenAPI, m, p, t)
    
    t.updateBounds(m)
    t.calcBaseWeight(m)
    t.calcMomentum(momFactor, m)
    t.calcCoinsToTrade(m, p)
    t.checkTradeSize(m, p, tradeFactor)
    
    cancelOrders(krakenAPI, t)    
    placeOrder(krakenAPI, m, t)

    printStatus(m, p, t, statusFileName, freezeFileName)
    printTermLine(m, p, t)
    printLogLine(m, p, t, logFileName)
    if abs(t.coinsToTrade) > 0:
        printLogLine(m, p, t, txFileName)
    drawPlot(m, t, plotFile)

    timeNow = datetime.datetime.now()
    delay   = (10 - (timeNow.minute)%10) * 60 - timeNow.second
    time.sleep(delay)
