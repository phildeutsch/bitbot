walkUp         = 0.15       # maxPrice = minPrice * (1 + walkUp): 0.15
walkDown       = 0          # minPrice = maxPrice * (1 - walkDown): 0
tradeFactor    = 0.00045    # minTrade = portfolioValue * tradeFactor: 0.00045
momFactor      = 0.75       # target   = target * (1-Momentum*momFactor): 0.75
priceWindow    = 100        # Window for weighted average

backupFund     = 0.00        # % of funds reserved for cheap buys: NA
backupLimit    = 1.00       # % of high for identifying cheap coins: NA
stopLossLimit  = 0.20       # % of high for liquidating all coins: NA
 
logFileName      = 'logs/history.csv'
statusFileName   = 'logs/status.txt'
plotFileName     = 'logs/plot.html'
txFileName       = 'logs/transactions.csv'

transFileName    = 'data/funding.csv'
logFileNameBT    = 'data/logBT.csv'
freezeFileName   = 'data/freeze.txt'
overrideFileName = 'data/override.txt'

emailAddress     = 'philipp.g.deutsch@gmail.com'
