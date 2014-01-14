##############################################################################
#                                                                            #
#   bitbot trader                                Philipp Deutsch             #
#                                                                            #
#                                                                            #
##############################################################################

from bbClasses import *
from bbSettings import *
from bbFunctions import *
import krakenex
import time
import sys
import re

t         = trader(logFileName, walkUp, walkDown, midDistance, tradeBuffer)
p         = portfolio(0,0)
m         = marketData('Null', 0, 0)
krakenAPI = krakenex.API(key, secret)

run = 1
while run:
    p, m = getData(krakenAPI, p, m, t)
    
    t.calcBaseWeight(m)
#   t.calcMomentum(m)
    t.calcCoinsToTrade(m, p)
    t.checkTradeSize(minTrade)
    
    cancelOrders(krakenAPI, t)    
        
    placeOrder(krakenAPI, m, t)

    printStatus(p, m, t, statusFileName)
    printTermLine(p, m, t)
    printLogLine(p, m, t, logFileName)

#   run = 0
    time.sleep(delay)
