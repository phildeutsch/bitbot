#!/usr/bin/python3
import datetime
import getopt
import time
import sys
import re

sys.path.append('./source')
sys.path.append('./api')

import bbCfg
import apiKraken
import apiBacktest
import bbClasses
import bbFunctions

from bbKeys import *

def main(argv=None):
    testFlag, btFlag, quiet = argParser(argv)
    
    # Use data from exchange
    if btFlag == 0:
        API = apiKraken.API(keyKraken, secKraken)
        t = bbClasses.trader(bbCfg.logFileName)
    # Backtest: Use data from logfile
    else:
        API = apiBacktest.API()
        with open(bbCfg.logFileNameBT, 'w') as logBT:
            logBT.write('Time,Bid,Ask,EUR,BTC,Trade,minPrice,maxPrice\n')
        t = bbClasses.trader(bbCfg.logFileNameBT)
    
    p = bbClasses.portfolio(100,0)
    m = bbClasses.marketData('Null', 500, 500)

    if btFlag == 1 and testFlag == 0 and not quiet:
    # Progress bar
        for i in range(bbFunctions.progressBarLength()):
            sys.stdout.write('|')
        sys.stdout.write('\n')
        sys.stdout.flush
    while True:
        mainLoop(m, p, t, API, testFlag, btFlag, quiet)

        if testFlag:
            break
        elif btFlag == 1 and API.line == bbFunctions.file_len(bbCfg.logFileName):
            break
    
        if not btFlag:       
            timeNow = datetime.datetime.now()
            delay = (10 - (timeNow.minute)%10) * 60 - timeNow.second
            time.sleep(delay)
    if not quiet:
        print('\n')      

def mainLoop(m, p, t, api, testFlag, btFlag, quiet):
    api.getBalance(m, p, t)
    api.getPrices(m, t, t.minTrade)
    
    if btFlag != 1:
        t.stopLoss(m, p)
    t.updateBounds(m)
    t.calcBaseWeight(m)
    t.calcMomentum(m)
    t.checkAllin(m, btFlag)
    t.checkOverride()
    
    t.calcCoinsToTrade(m, p)
    t.checkTradeSize(m, p)
 
    if testFlag == 1:
        bbFunctions.printTermLine(m, p, t)
    elif btFlag == 1:
        bbFunctions.printLogLine(m, p, t, bbCfg.logFileNameBT, bounds = 1)
        if api.line %  bbCfg.progressBar == 0 and not quiet:
            sys.stdout.write('|')
            sys.stdout.flush()
    else:
        if t.suspend == 1:
            print('Trading suspended!')
        elif t.suspend == 0 and t.error == 0:
            api.cancelOrders(t)
            api.placeOrder(m, t)
        
        bbFunctions.printTermLine(m, p, t)
        bbFunctions.printStatus(m, p, t)
        bbFunctions.printLogLine(m, p, t, bbCfg.logFileName)
        bbFunctions.drawPlot(m, t)
        if abs(t.coinsToTrade) > 0:
            bbFunctions.printLogLine(m, p, t, bbCfg.txFileName)
            
        if t.error != 0:
            t.handle_error(m)
        
def argParser(argv):
    testFlag = 0
    btFlag = 0
    quiet  = 0

    if argv is None:
        argv = sys.argv[1:]
    else:
        argv = argv.split()
    opts, args = getopt.getopt(argv, 'btq')
    for o, a in opts:
        if o == '-b':
            btFlag = 1
        elif o == '-t':
            testFlag = 1
        elif o == '-q':
            quiet = 1
    
    return testFlag, btFlag, quiet

if __name__ == "__main__":
    main()
