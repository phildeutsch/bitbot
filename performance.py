from bbSettings import *
from bbPerformance import *

logFileNameBT  = 'Logs/' + str(tradeBuffer)
logFileNameBT += str(priceWindow)
logFileNameBT += str(momFactor)
logFileNameBT += str(midDistance)
logFileNameBT += str(walkUp)
logFileNameBT += str(walkDown)
logFileNameBT += str(tradeFactor) + '.csv'
                            
#makePerformanceTable(logFileName, transferFile)
makePerformanceTable(logFileNameBT)
