import sys
sys.path.append('./source')
from bbSettings import *
from bbPerformance import *

startDate = '2014-01-08'

btflag  = str(sys.argv[1])
endDate = str(sys.argv[2])

if len(endDate) is not 10:
    endDate = None

getTransactions(logFileName, transFileName)
if btflag is '1':
    import backtest
    logFileNameBT  = 'data/' + str(tradeBuffer)
    logFileNameBT += str(priceWindow)
    logFileNameBT += str(momFactor)
    logFileNameBT += str(midDistance)
    logFileNameBT += str(walkUp)
    logFileNameBT += str(walkDown) + '.csv'
    makePerformanceTable(logFileName, logFileNameBT, startDate, endDate, transFileName)
else:
    makePerformanceTable(logFileName, None, startDate, endDate, transFileName)
    
