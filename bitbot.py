###############################################################################
#                                                                             #
#   bitbot trader                                Philipp Deutsch              #
#                                                                             #
#                                                                             #
###############################################################################

from bbKeys import *
from bbClasses import *
from bbSettings import *
from bbFunctions import *
import krakenex
import time
import sys
import re

t         = trader(logFileName, walkUp, walkDown, midDistance, tradeBuffer)
p         = portfolio(funds,0)
m         = marketData('Null', 0, 0, priceWindow)
krakenAPI = krakenex.API(key, secret)

while True:
    p, m = getData(krakenAPI, p, m, t)
    
    t.calcBaseWeight(m)
    t.calcMomentum(momFactor, m)
    t.calcCoinsToTrade(m, p)
    t.checkTradeSize(minTrade)
    
    cancelOrders(krakenAPI, t)    
    placeOrder(krakenAPI, m, t)

    printStatus(p, m, t, statusFileName)
    printTermLine(p, m, t)
    printLogLine(p, m, t, logFileName)

    t = trader(logFileNameBT, walkUp, walkDown, midDistance, tradeBuffer)

    time.sleep(delay)
