import sys
import cmd
sys.path.append('./source')
sys.path.append('./api')

from bbSettings import *
from bbPerformance import *

class bbCmd(cmd.Cmd):
    def __init__(self):
        cmd.Cmd.__init__(self)
        self.prompt = 'B> '

    
    def do_performance(self, arg):
        startDate = input('Initial Date (YYYY-MM-DD): ')
        if len(startDate) is not 10:
            startDate = '2014-01-08'
        endDate   = input('End Date (YYYY-MM-DD): ')
        if len(endDate) is not 10:
            endDate = None
        btflag    = 0
        getTransactions(logFileName, transFileName)
        if btflag is '1':
            import backtest
            logFileNameBT  = 'data/' + str(tradeBuffer)
            logFileNameBT += str(priceWindow)
            logFileNameBT += str(momFactor)
            logFileNameBT += str(midDistance)
            logFileNameBT += str(walkUp)
            logFileNameBT += str(walkDown) + '.csv'
            makePerformanceTable(logFileName, logFileNameBT, startDate,
                                 endDate, transFileName)
        else:
            makePerformanceTable(logFileName, None, startDate, endDate,
                                 transFileName)        
    def help_performance(self):
            print('Syntax: performance')
            print('-- Calculates the performance between two dates for ' +
                  'a client')
            

    def do_exit(self, arg):
        sys.exit(1)
        
    def help_exit(self):
            print('Syntax: exit')
            print('-- Terminates the application')
