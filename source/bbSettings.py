WALKUP         = 0.15       # maxPrice = minPrice * (1 + walkUp): 0.15
WALKDOWN       = 0          # minPrice = maxPrice * (1 - walkDown): 0
TRADEFACTOR    = 0.00045    # minTrade = portfolioValue * tradeFactor: 0.00045
MOMFACTOR      = 0.75       # target   = target * (1-Momentum*momFactor): 0.75
PRICEWINDOW    = 100        # Window for weighted average

BACKUPFUND     = 0.20        # % of funds reserved for cheap buys: NA
ALLINLIMIT     = 0.10       # % of high for identifying cheap coins: NA
STOPLOSSLIMIT  = 0.20       # % of high for liquidating all coins: NA
 
LOGFILENAME      = 'logs/history.csv'
STATUSFILENAME   = 'logs/status.txt'
PLOTFILENAME     = 'logs/plot.html'
TXFILENAME       = 'logs/transactions.csv'

TRANSFILENAME    = 'data/funding.csv'
LOGFILENAMEBT    = 'data/logBT.csv'
FREEZEFILENAME   = 'data/freeze.txt'
OVERRIDEFILENAME = 'data/override.txt'

EMAILADDRESS     = 'philipp.g.deutsch@gmail.com'
