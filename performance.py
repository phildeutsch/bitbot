from bbSettings import *
from bbPerformance import *

logFileNameBT  = 'Logs/' + str(tradeBuffer)
logFileNameBT += str(priceWindow)
logFileNameBT += str(momFactor)
logFileNameBT += str(midDistance)
logFileNameBT += str(walkUp)
logFileNameBT += str(walkDown) + '.csv'
                            
startDate = '2014-01-08'
endDate   = '2014-01-20'

makePerformanceTable(logFileName, logFileNameBT, startDate, endDate, transferFile)
