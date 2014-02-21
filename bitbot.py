#!/usr/bin/python3
import datetime
import getopt
import time
import sys
import re

sys.path.append('./source')
sys.path.append('./api')

import apiKraken
import apiBacktest
import bbClasses
import bbFunctions

from bbKeys import *
from bbSettings import *

def main(argv=None):
    testFlag, btFlag = argParser(argv)

    # Use data from exchange
    if btFlag == 0:
        API = apiKraken.API(keyKraken, secKraken)
        t   = bbClasses.trader(logFileName, walkUp, walkDown, priceWindow, tradeFactor, 
                     momFactor, backupFund, allinLimit, stopLossLimit)
    # Use data from logfile
    else:
        API = apiBacktest.API(logFileName)
        with open(logFileNameBT, 'w') as logBT:
            logBT.write('Time,Bid,Ask,EUR,BTC,Trade,minPrice,maxPrice\n')
        t   = bbClasses.trader(logFileNameBT, walkUp, walkDown, priceWindow, tradeFactor, 
                     momFactor, backupFund, allinLimit, stopLossLimit)

    p         = bbClasses.portfolio(100,0)
    m         = bbClasses.marketData('Null', 500, 500, priceWindow)

    while True:
        mainLoop(m, p, t, API, testFlag, btFlag)

        if testFlag == 1:
            break
        elif btFlag == 1 and API.line == bbFunctions.file_len(logFileName):
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
        bbFunctions.printTermLine(m, p, t)
    elif btFlag == 1:
        bbFunctions.printLogLine(m, p, t, logFileNameBT, bounds = 1)
        if abs(t.coinsToTrade) > 0:
            bbFunctions.printTermLine(m, p, t)
    else:
        if t.suspend != 1:
            print('Trading suspended!')
            api.cancelOrders(t)
            api.placeOrder(m, t)

        bbFunctions.printTermLine(m, p, t)
        bbFunctions.printStatus(m, p, t, statusFileName, freezeFileName)
        bbFunctions.printLogLine(m, p, t, logFileName)
        bbFunctions.drawPlot(m, t, plotFileName)
        if abs(t.coinsToTrade) > 0:
            bbFunctions.printLogLine(m, p, t, txFileName)

        if t.error != 0:
            t.handle_error(m, emailAddress, errorFileName)

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
