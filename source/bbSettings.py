walkUp         = 0.15       # maxPrice = minPrice * (1 + walkUp): 0.15
walkDown       = 0          # minPrice = maxPrice * (1 - walkDown): 0
tradeFactor    = 0.00045    # minTrade = portfolioValue * tradeFactor: 0.00045
momFactor      = 0.75       # target   = target * (1-Momentum*momFactor): 0.75
priceWindow    = 100        # Window for weighted average

buyCheapFund   = 0.2        # Percentage of funds reserved for cheap buys
buyCheapLimit  = 0.05       # Limit (from last high) to identifying cheap coins
stopLossLimit  = 0.10       # Limit (from last high) to liquidate all coins
 
logFileName      = 'logs/history.csv'
statusFileName   = 'logs/status.txt'
plotFile         = 'logs/plot.html'
txFileName       = 'logs/transactions.csv'

transFileName    = 'data/funding.csv'
logFileNameBT    = 'data/logBT.csv'
freezeFileName   = 'data/freeze.txt'
overrideFileName = 'data/override.txt'

emailAddress     = 'philipp.g.deutsch@gmail.com'
