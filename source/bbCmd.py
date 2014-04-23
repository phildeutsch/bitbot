import sys
import cmd
import datetime
import numpy as np
from imp import reload
sys.path.append('./source')
sys.path.append('./api')

import bbCfg
import apiKraken
import bitbot
import bbClasses
import bbPerformance
import bbFunctions

from bbKeys import *

class Cmd(cmd.Cmd):
    def __init__(self):
        cmd.Cmd.__init__(self)
        self.prompt = 'B> '

    def do_funding(self, arg):
        krakenAPI = apiKraken.API(keyKraken, secKraken)
        pKraken   = bbClasses.portfolio(1,0)
        mKraken   = bbClasses.marketData('Null', 0, 0)
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
        with open(bbCfg.fundFileName, 'at') as ff:
            ff.write(writeList)

    def help_funding(self):
        print('Syntax: funding')
        print('-- Input a cash flow to/from the portfolio')
            
    def do_calibrate(self, arg):
        reload(bbCfg)
        old_walkUp = bbCfg.walkUp
        old_tradeFactor = bbCfg.tradeFactor
        old_allinLimit = bbCfg.allinLimit
        old_backupFund = bbCfg.backupFund
        m = [0.9, 1.1]
        result = []
        numLinesLog = bbFunctions.file_len(bbCfg.logFileName)
        for i in range(len(m)**4):
            sys.stdout.write('|')
        sys.stdout.write('\n')
        for bbCfg.walkUp in [x * old_walkUp for x in m]:
            for bbCfg.tradeFactor in [x * old_tradeFactor for x in m]:
                for bbCfg.allinLimit in [x * old_allinLimit for x in m]:
                    for bbCfg.backupFund in [x * old_backupFund for x in m]:
                        bbCfg.logFileNameBT = bbFunctions.getLogFileNameBT()
                        try:
                            n = bbFunctions.file_len(bbCfg.logFileNameBT)
                        except:
                            n = 0
                        #bbFunctions.display_config()
                        sys.stdout.write('|')
                        if n != numLinesLog:
                            bitbot.main('-b')
                        d,r=bbPerformance.getReturns(bbCfg.logFileNameBT, 
                                                     None, '2014-01-08', None)
                        result.append([
                                bbCfg.walkUp,
                                bbCfg.tradeFactor,
                                bbCfg.allinLimit,
                                bbCfg.backupFund,
                                100*bbPerformance.totalReturn(r[:,3])])
        print('')
        result = np.array(result)
        result = result[np.argsort(result[:, len(result[0])-1])]
        print(' '.join('{0:>10}'.format(x) for x in ['walkUp', 'tradeFactor', 'allinLimit', 'backupFund', 'Return']))
        for row in result[-10:]:
            print(' '.join('{0:10.4}'.format(x) for x in row))
        
    def help_calibrate(self):
            print('Syntax: calibrate')
            print('-- Optimize current parameters')

    def do_backtest(self, arg):
        paramFlag = input('Use current parameters? ([y]/n): ')
        if paramFlag is 'n':
        #   Change parameters here
            bbFunctions.choose_parameters()
        numLinesLog = bbFunctions.file_len(bbCfg.logFileName) 
        bbCfg.logFileNameBT = bbFunctions.getLogFileNameBT()
        try:
            numLinesLogBT = bbFunctions.file_len(bbCfg.logFileNameBT)
        except:
            numLinesLogBT = 0
        if numLinesLogBT != numLinesLog:
            bitbot.main('-b')
        d,r=bbPerformance.getReturns(bbCfg.logFileNameBT, None, '2014-01-08', None)
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
        chooseBT = input('Calculate performance for backtest? y/[n]: ')
        if chooseBT == 'y':
            bbCfg.logFileNameBT = bbFunctions.getLogFileNameBT() 
            d,r=bbPerformance.getReturns(bbCfg.logFileNameBT, None,
                                         startDate, endDate)
        else:
            d,r=bbPerformance.getReturns(bbCfg.logFileName, bbCfg.fundFileName,
                                         startDate, endDate)
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
        mKraken   = bbClasses.marketData('Null', 0, 0)
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
