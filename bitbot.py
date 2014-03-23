#!/usr/bin/python3
import datetime
import getopt
import time
import sys
import re
import math

sys.path.append('./source')
sys.path.append('./api')

import apiKraken
import apiBacktest
import bbClasses
import bbFunctions

from bbKeys import *
from bbSettings import *

def main(argv=None):
    testFlag, btFlag, vbFlag, debugFlag = argParser(argv)

    # Use data from exchange
    if btFlag == 0:
        API = apiKraken.API(keyKraken, secKraken)
        t = bbClasses.trader(logFileName, walkUp, walkDown, priceWindow, 
                             tradeFactor,  momFactor, backupFund, allinLimit, 
                             stopLossLimit)
    # Use data from logfile
    else:
        API = apiBacktest.API(logFileName)
        with open(logFileNameBT, 'w') as logBT:
            logBT.write('Time,Bid,Ask,EUR,BTC,Trade,minPrice,maxPrice\n')
        t = bbClasses.trader(logFileNameBT, walkUp, walkDown, priceWindow,
                             tradeFactor, momFactor, backupFund, allinLimit, 
                             stopLossLimit)

    p = bbClasses.portfolio(100,0)
    m = bbClasses.marketData('Null', 500, 500, priceWindow)

    if btFlag == 1 and vbFlag == 0 and testFlag == 0:
    # Progress bar
        for i in range(math.floor(bbFunctions.file_len(logFileName)/200)):
            sys.stdout.write('|')
        sys.stdout.write('\n')
        sys.stdout.flush
    while True:
        mainLoop(m, p, t, API, testFlag, btFlag, vbFlag, debugFlag)

        if testFlag:
            break
        elif btFlag == 1 and API.line == bbFunctions.file_len(logFileName):
            break
    print('\n')

def mainLoop(m, p, t, api, testFlag, btFlag, vbFlag, debugFlag):
    api.getBalance(m, p, t)
    api.getPrices(m, t, t.minTrade)
    
    if btFlag != 1:
        t.stopLoss(m, p, overrideFileName)
    if debugFlag:
        sys.stdout.write(datetime.datetime.now().isoformat()[0:19] + '\t')
        sys.stdout.write('Updating bounds...')
        sys.stdout.flush()
    t.updateBounds(m)
    if debugFlag:
        sys.stdout.write('done.\t' + str(t.minTrade) + ' ' + str(t.maxTrade)+ '\n')
        sys.stdout.write(datetime.datetime.now().isoformat()[0:19] + '\t')
        sys.stdoue.write('Calculating base weight...')
        sys.stdout.flush()
    t.calcBaseWeight(m)
    if debugFlag:
        sys.stdout.write('done.\t' + '\n')
        sys.stdout.write(datetime.datetime.now().isoformat()[0:19] + '\t')
        sys.stdout.write('Calculating momentum...')
        sys.stdout.flush()
    t.calcMomentum(m)
    if debugFlag:
        sys.stdout.write('done.\nChecking all-in...')
        sys.stdout.write(datetime.datetime.now().isoformat()[0:19] + '\t')
        sys.stdout.flush()
    t.checkAllin(m, btFlag)
    if debugFlag:
        sys.stdout.write('done.\nChecking override...')
        sys.stdout.write(datetime.datetime.now().isoformat()[0:19] + '\t')
        sys.stdout.flush()
    t.checkOverride(overrideFileName)
    
    if debugFlag:
        sys.stdout.write('done.\nCalculating coins to trade...')
        sys.stdout.write(datetime.datetime.now().isoformat()[0:19] + '\t')
        sys.stdout.flush()
    t.calcCoinsToTrade(m, p)
    if debugFlag:
        sys.stdout.write('done.\nChecking trade size...')
        sys.stdout.write(datetime.datetime.now().isoformat()[0:19] + '\t')
        sys.stdout.flush()
    t.checkTradeSize(m, p, tradeFactor)
    if debugFlag:
        sys.stdout.write('done.\n')
        sys.stdout.write(datetime.datetime.now().isoformat()[0:19] + '\t')
        sys.stdout.flush()
 
    if testFlag == 1:
        bbFunctions.printTermLine(m, p, t)
    elif btFlag == 1:
        bbFunctions.printLogLine(m, p, t, logFileNameBT, bounds = 1)
        if vbFlag == 1:
            if abs(t.coinsToTrade) > 0:
                bbFunctions.printTermLine(m, p, t)
        elif vbFlag == 0:
            if api.line % 200 == 0:
                sys.stdout.write('|')
                sys.stdout.flush()
    else:
        if t.suspend == 1:
            print('Trading suspended!')
        elif t.suspend == 0 and t.error == 0:
            if debugFlag:
                sys.stdout.write('Cancelling orders...')
                sys.stdout.flush()
            api.cancelOrders(t)
            if debugFlag:
                sys.stdout.write('done.\nPlacing orders...')
                sys.stdout.flush()
            api.placeOrder(m, t)
            if debugFlag:
                sys.stdout.write('done.\n')
                sys.stdout.write(datetime.datetime.now().isoformat()[0:19] + '\t')
                sys.stdout.flush()
        
        if debugFlag:
            sys.stdout.write('Logging...')
            sys.stdout.flush()
        else:
            bbFunctions.printTermLine(m, p, t)
        bbFunctions.printStatus(m, p, t, statusFileName, freezeFileName)
        bbFunctions.printLogLine(m, p, t, logFileName)
        bbFunctions.drawPlot(m, t, plotFileName)
        if abs(t.coinsToTrade) > 0:
            bbFunctions.printLogLine(m, p, t, txFileName)
        if debugFlag:
            sys.stdout.write('done\n')
            sys.stdout.write(datetime.datetime.now().isoformat()[0:19] + '\t')
            sys.stdout.flush()
            
        if debugFlag:
            sys.stdout.write('Error handling...')
            sys.stdout.flush()
        if t.error != 0:
            t.handle_error(m, emailAddress, errorFileName)
        if debugFlag:
            sys.stdout.write('done.\n')
            sys.stdout.write(datetime.datetime.now().isoformat()[0:19] + '\t')
            sys.stdout.flush()

        if debugFlag:
            sys.stdout.write('Calculating seconds to sleep...')
            sys.stdout.flush()
        timeNow = datetime.datetime.now()
        delay = (10 - (timeNow.minute)%10) * 60 - timeNow.second
        if debugFlag:
            sys.stdout.write('done. \t(' + str(delay) + ').\n\n')
            sys.stdout.write(datetime.datetime.now().isoformat()[0:19] + '\t')
            sys.stdout.flush()

        time.sleep(delay)
        
def argParser(argv):
    testFlag = 0
    btFlag = 0
    vbFlag = 0
    debugFlag = 0

    if argv is None:
        argv = sys.argv[1:]
    else:
        argv = argv.split()
    opts, args = getopt.getopt(argv, 'btvd')
    for o, a in opts:
        if o == '-b':
            btFlag = 1
        elif o == '-t':
            testFlag = 1
        elif o == '-v':
            vbFlag = 1
        elif o == '-d':
            debugFlag = 1
    
    return testFlag, btFlag, vbFlag, debugFlag

if __name__ == "__main__":
    main()
