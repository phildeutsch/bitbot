import sys
import cmd
sys.path.append('./source')
sys.path.append('./api')

import api
import bitbot
from bbClasses import *
from bbSettings import *
from bbFunctions import *
from bbPerformance import *
from bbKeysMonitor import *

class bbCmd(cmd.Cmd):
    def __init__(self):
        cmd.Cmd.__init__(self)
        self.prompt = 'B> '

    def do_backtest(self, arg):
        paramFlag = input('Use current parameters? ([y]/n): ')
        if paramFlag is not 'n':
            bitbot.main('-b')
        d,r=getReturns(logFileNameBT, None, '2014-01-01', None)
        printSummary(r)
            
    def help_backtest(self):
        print('Syntax: backtest')
        print('-- Run backtest using the current logfile as input')
    
    
    def do_performance(self, arg):
        startDate = input('Initial Date (YYYY-MM-DD): ')
        if len(startDate) is not 10:
            startDate = '2014-01-08'
        endDate   = input('End Date (YYYY-MM-DD): ')
        if len(endDate) is not 10:
            endDate = None
        btflag = input('Run backtest? (y/[n]): ')
        getTransactions(logFileName, transFileName)
        if btflag is 'y':
            d,r=getReturns(logFileNameBT, None, startDate, endDate)
            printReturns(d, r)
            print('')
            printSummary(r)
        else:
            d,r=getReturns(logFileName, transFileName, startDate, endDate)
            printReturns(d, r)
            print('')
            printSummary(r)
            
    def help_performance(self):
            print('Syntax: performance')
            print('-- Calculates the performance between two dates for ' +
                  'a client')


    def do_balance(self, arg):    
        krakenAPI = api.kraken.API(keyKraken, secKraken)
        pKraken   = portfolio(1,0)
        mKraken   = marketData('Null', 0, 0, 0)
        mKraken, pKraken = getData(krakenAPI, mKraken, pKraken)

        print('Exchange   EUR         BTC     Value  ')
        print('--------------------------------------')
        sys.stdout.write('{0:<10}'.format('Kraken'))       
        sys.stdout.write('{0:>8.2f}'.format(float(pKraken.EUR)))       
        sys.stdout.write('{0:>10.3f}'.format(float(pKraken.BTC)))
        sys.stdout.write('{0:>10.2f}'.format(pKraken.BTC * mKraken.bid + \
                                             pKraken.EUR))
        print('')       


    def help_balance(self):
            print('Syntax: balance')
            print('-- Shows the current balance and total Value of the ' +
                  'portfolio')
            
    def do_exit(self, arg):
        sys.exit(1)
        
    def help_exit(self):
            print('Syntax: exit')
            print('-- Terminates the application')
