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
import os.path

t         = trader(logFileName, walkUp, walkDown, midDistance, tradeBuffer)
p         = portfolio(0,0)
m         = marketData('Null', 0, 0)
krakenAPI = krakenex.API(key, secret)

run = 1
while run:
    p, m = getData(krakenAPI, p, m)
    
    t.calcBaseWeight(m)
#   t.calcMomentum(m)
    t.calcCoinsToTrade(m, p)
    t.checkTradeSize(minTrade)
    
    cancelOrders(krakenAPI)    
        
    placeOrder(krakenAPI, m, t)

    strLog = m.time
    strLog = strLog + ' | B: '+str(round(m.bid,1))+' A: '+str(round(m.ask,1))
    strLog = strLog + ' | EUR: ' + str(p.EUR) + ' | BTC: ' + str(round(p.BTC,3))
    strLog = strLog + ' | Bounds: ' + str(t.minPrice) + ' ' + str(t.maxPrice)
    strLog = strLog + ' | Trade: ' + str(round(t.coinsToTrade,3)) + '\n'

    # Write user information + Log
    sys.stdout.write(strLog)
    sys.stdout.flush()

    printLogLine(p, m, t, logFileName)
#   run = 0
    time.sleep(delay)
