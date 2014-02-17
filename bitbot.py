#!/usr/bin/python3

import sys
sys.path.append('./source')
sys.path.append('./api')
import api
import bbClasses
import bbFunctions

from bbKeys import *
from bbSettings import *

import datetime
import getopt
import time
import re

def main(argv=None):
    testFlag, btFlag = argParser(argv)

    testFlag = 1

    # Use data from exchange
    if btFlag == 0:
        API = api.kraken.API(keyKraken, secKraken)
        t   = bbClasses.trader(LOGFILENAME, WALKUP, WALKDOWN, PRICEWINDOW, TRADEFACTOR, 
                     MOMFACTOR, BACKUPFUND, ALLINLIMIT, STOPLOSSLIMIT)
    # Use data from logfile
    else:
        API = api.backtest.API(LOGFILENAME)
        with open(LOGFILENAMEBT, 'w') as logBT:
            logBT.write('Time,Bid,Ask,EUR,BTC,Trade,minPrice,maxPrice\n')
        t   = bbClasses.trader(LOGFILENAMEBT, WALKUP, WALKDOWN, PRICEWINDOW, TRADEFACTOR, 
                     MOMFACTOR, BACKUPFUND, ALLINLIMIT, STOPLOSSLIMIT)
    p         = bbClasses.portfolio(100,0)
    m         = bbClasses.marketData('Null', 500, 500, PRICEWINDOW)

    while True:
        mainLoop(m, p, t, API, testFlag, btFlag)

        if testFlag == 1:
            break
        if btFlag == 1 and API.line == bbFunctions.file_len(LOGFILENAME):
            break

def mainLoop(m, p, t, api, testFlag, btFlag):
    api.getBalance(m, p, t)
    api.getPrices(m, t.minTrade)
    
    if btFlag != 1:
        t.stopLoss(m, p, OVERRIDEFILENAME)
    t.updateBounds(m)
    t.calcBaseWeight(m)
    t.calcMomentum(m)
    t.checkAllin(m, btFlag)
    t.checkOverride(OVERRIDEFILENAME)
    
    t.calcCoinsToTrade(m, p)
    t.checkTradeSize(m, p, TRADEFACTOR)
 
    if testFlag == 1:
        bbFunctions.printTermLine(m, p, t)
    elif btFlag == 1:
        bbFunctions.printLogLine(m, p, t, LOGFILENAMEBT, bounds = 1)
        if abs(t.coinsToTrade) > 0:
            bbFunctions.printTermLine(m, p, t)

    else:
        if t.suspend != 1:
            api.cancelOrders(t)
            api.placeOrder(m, t)

        bbFunctions.printTermLine(m, p, t)
        bbFunctions.printStatus(m, p, t, STATUSFILENAME, FREEZEFILENAME)
        bbFunctions.printLogLine(m, p, t, LOGFILENAME)
        bbFunctions.drawPlot(m, t, PLOTFILENAME)
        if abs(t.coinsToTrade) > 0:
            bbFunctions.printLogLine(m, p, t, TXFILENAME)

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
