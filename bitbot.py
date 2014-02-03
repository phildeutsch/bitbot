import sys
sys.path.append('./source')
sys.path.append('./api')

from bbKeys import *
from bbClasses import *
from bbSettings import *
from bbFunctions import *
import APIkraken

import time
import re

t         = trader(logFileName, walkUp, walkDown, midDistance, tradeBuffer, 
                   priceWindow)
p         = portfolio(1,0)
m         = marketData('Null', 0, 0, priceWindow)
krakenAPI = APIkraken.API(key, secret)

while True:
    t    = trader(logFileName, walkUp, walkDown, midDistance, tradeBuffe,
                  priceWindow)
    m, p = getData(krakenAPI, m, p, t)
    
    t.calcBaseWeight(m)
    t.calcMomentum(momFactor, m)
    t.calcCoinsToTrade(m, p)
    t.checkTradeSize(m, p, tradeFactor)
    
    cancelOrders(krakenAPI, t)    
    placeOrder(krakenAPI, m, t)

    printStatus(m, p, t, statusFileName)
    printTermLine(m, p, t)
    printLogLine(m, p, t, logFileName)
    if abs(t.coinsToTrade) > 0:
        printLogLine(m, p, t, txFileName)
    drawPlot(plotFileHead, plotFileTail, m, t)

    time.sleep(delay)
