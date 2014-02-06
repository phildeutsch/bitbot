import sys
import cmd
sys.path.append('./source')
sys.path.append('./api')

import apiKraken
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
        stepSize  = input('Set step size [10]: ')
        try:
            stepSize = int(stepSize)
        except:
            stepSize = 10
        paramFlag = input('Use current parameters? ([y]/n): ')
        if paramFlag is not 'n':
            import backtest
            
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
        btflag = input('Run backtest? (y/n): ')
        getTransactions(logFileName, transFileName)
        if btflag is 'y':
            logFileNameBT  = 'data/' + str(tradeBuffer)
            logFileNameBT += str(priceWindow)
            logFileNameBT += str(momFactor)
            logFileNameBT += str(midDistance)
            logFileNameBT += str(walkUp)
            logFileNameBT += str(walkDown) + '.csv'
            makePerformanceTable(logFileName, logFileNameBT, startDate,
                                 endDate, transFileName)
        else:
            rbh, sbh, rst, sst = makePerformanceTable(logFileName, None,
                                     startDate, endDate, transFileName)
            
    def help_performance(self):
            print('Syntax: performance')
            print('-- Calculates the performance between two dates for ' +
                  'a client')


    def do_balance(self, arg):    
        krakenAPI = apiKraken.API(keyKraken, secKraken)
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
