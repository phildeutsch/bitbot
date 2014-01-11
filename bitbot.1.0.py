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
import pandas as pd
import numpy as np

t         = trader(logFileName)
p         = portfolio(0,0)
m         = marketData('Null', 0, 0)
krakenAPI = krakenex.API(key, secret)

run = 1
while run:
    [p, m] = getData(krakenAPI, p, m)
    
    print m.mean    
    print t.calcBaseWeight(m)
    print t.calcMomentum(m)
    print t.calcCoinsToTrade(m, p)
    print t.checkTradeSize()
    
#   cancelOrders(krakenAPI)    
        
#   placeOrder(krakenAPI, t)

    strLog = m.time
    strLog = strLog + ' | B: '+str(round(m.bid,1))+' A: '+str(round(m.ask,1))
    strLog = strLog + ' | EUR: ' + str(p.EUR) + ' | BTC: ' + str(round(p.BTC,3))
    strLog = strLog + ' | Bounds: ' + str(t.minPrice) + ' ' + str(t.maxPrice)
    strLog = strLog + ' | Trade: ' + str(round(t.coinsToTrade,3)) + '\n'

#   Update trader parameters

    # Write user information + Log
    sys.stdout.write(strLog)
    sys.stdout.flush()

#   printLogLine(p, m, t, logFileName)
#    time.sleep(600)
    run = 0
