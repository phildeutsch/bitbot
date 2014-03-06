import sys
import cmd
import datetime
sys.path.append('./source')
sys.path.append('./api')

import apiKraken
import bitbot
import bbClasses
import bbPerformance

from bbKeys import *
from bbSettings import *

class Cmd(cmd.Cmd):
    def __init__(self):
        cmd.Cmd.__init__(self)
        self.prompt = 'B> '

    def do_funding(self, arg):
        krakenAPI = apiKraken.API(keyKraken, secKraken)
        pKraken   = bbClasses.portfolio(1,0)
        mKraken   = bbClasses.marketData('Null', 0, 0, 0)
        b,a = krakenAPI.getDepth(1)
        mKraken.bid = float(b[0][0])
        mKraken.ask = float(a[0][0])

        strTime = datetime.datetime.now().isoformat()[0:16]
        flagBTC = input('Enter BTC transaction? ([y]/n): ')
        if flagBTC is 'n':
            amtEUR = input('Enter EUR amount: (<0 if withdrawal): ')
            writeList = ','.join([strTime, str(mKraken.bid), str(mKraken.ask),
                                  '0', str(amtEUR) + '\n'])
        else:
            amtBTC = input('Enter BTC amount: (<0 if withdrawal): ')
            writeList = ','.join([strTime, str(mKraken.bid), str(mKraken.ask),
                                  str(amtBTC), '0\n'])
        with open(fundFileName, 'at') as ff:
            ff.write(writeList)

    def help_funding(self):
            print('Syntax: funding')
            print('-- Input a cash flow to/from the portfolio')

    def do_backtest(self, arg):
        paramFlag = input('Use current parameters? ([y]/n): ')
        vbFlag = input('Show trades? (y/[n]): ')
        if paramFlag is 'n':
        #   Change parameters here
            params = 1
        if vbFlag is 'y':
            bitbot.main('-b -v')
        else:
            bitbot.main('-b')
        d,r=bbPerformance.getReturns(logFileNameBT, None, '2014-01-01', None)
        bbPerformance.printSummary(r)
            
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
        if btflag is 'y':
            d,r=bbPerformance.getReturns(logFileNameBT, None, startDate, endDate)
            bbPerformance.printReturns(d, r)
            print('')
            bbPerformance.printSummary(r)
        else:
            d,r=bbPerformance.getReturns(logFileName, fundFileName, startDate, endDate)
            bbPerformance.printReturns(d, r)
            print('')
            bbPerformance.printSummary(r)
            
    def help_performance(self):
            print('Syntax: performance')
            print('-- Calculates the performance between two dates for ' +
                  'a client')


    def do_balance(self, arg):    
        krakenAPI = apiKraken.API(keyKraken, secKraken)
        pKraken   = bbClasses.portfolio(1,0)
        mKraken   = bbClasses.marketData('Null', 0, 0, 0)
        b,a = krakenAPI.getDepth(1)
        mKraken.bid = float(b[0][0])
        mKraken.ask = float(a[0][0])
        krakenAPI.getBalance(mKraken, pKraken)

        print('Exchange   EUR         BTC     Value  ')
        print('--------------------------------------')
        sys.stdout.write('{0:<10}'.format('Kraken'))       
        sys.stdout.write('{0:>8.2f}'.format(float(pKraken.EUR)))       
        sys.stdout.write('{0:>10.3f}'.format(float(pKraken.BTC)))
        sys.stdout.write('{0:>10.2f}'.format(pKraken.value))
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
