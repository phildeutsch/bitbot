###############################################################################
#                                                                             #
#   bitbot trader                                Philipp Deutsch              #
#                                                                             #
#                                                                             #
###############################################################################

import sys
sys.path.append('./source')
from bbKeys import *
from bbClasses import *
from bbSettings import *
from bbFunctions import *
import krakenex
import time
import re

t         = trader(logFileName, walkUp, walkDown, midDistance, tradeBuffer, priceWindow)
p         = portfolio(1,0)
m         = marketData('Null', 0, 0, priceWindow)
krakenAPI = krakenex.API(key, secret)

while True:
    t    = trader(logFileName, walkUp, walkDown, midDistance, tradeBuffer, priceWindow)
    m, p = getData(krakenAPI, m, p, t)
    
    t.calcBaseWeight(m)
    t.calcMomentum(momFactor, m)
    t.calcCoinsToTrade(m, p)
    t.checkTradeSize(m, p, tradeFactor)
    
    cancelOrders(krakenAPI, t)    
    placeOrder(krakenAPI, m, t)

    printStatus(p, m, t, statusFileName)
    printTermLine(p, m, t)
    printLogLine(p, m, t, logFileName)
    if t.coinsToTrade > 0:
        printLogLine(p, m, t, txFileName)
    drawPlot(plotFileHead, plotFileTail, m, t)

    time.sleep(delay)
