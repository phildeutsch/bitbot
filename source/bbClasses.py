import bbFunctions
from collections import deque

class portfolio:
    """ Stores portfolio with holdings in EUR and BTC """

    def __init__(self, amountEUR, amountBTC):
        self.EUR = amountEUR
        self.BTC = amountBTC
        self.weight = 1
        self.value = 0

class marketData:
    """ Stores market data """

    def __init__(self, time, bid, ask, priceWindow):
        self.time = time
        self.bid = bid
        self.ask = ask
        self.price = (bid + ask)/2
        self.histPrices = deque([], priceWindow)
        self.mean = self.price
        self.low = self.price
        self.high = self.price

class trader:
    """ Stores all trade parameters """
    
    def __init__(self, logFileName, walkUp, walkDown, priceWindow, tradeFactor,
                 momFactor, backupFund, allinLimit, stopLossLimit):
        try:
            self.minPrice, self.maxPrice = bbFunctions.getBounds(logFileName, walkUp, walkDown)
        except:
            self.minPrice = 0
            self.maxPrice = 0
        self.walkUp = walkUp
        self.walkDown = walkDown
        self.coinsToTrade = 0
        self.target = 1
        self.tradePrice = 1
        self.override = 0
        self.suspend = 0
        self.minTrade = 0
        self.tradeFactor = tradeFactor
        self.momFactor = momFactor
        self.allinFlag = 0
        self.backupFund = backupFund
        self.allinLimit = allinLimit
        self.stopLossLimit = stopLossLimit
        self.buys  = deque([], priceWindow)
        self.sells = deque([], priceWindow)
        self.error = 0

    def checkOverride(self, overrideFileName):
        try:
            with open(overrideFileName, 'rt') as of:
                data = of.readlines()
            flagOverride   = int(data[0].split('=')[-1].strip())
            targetOverride = int(data[1].split('=')[-1].strip())
            flagSuspend    = int(data[2].split('=')[-1].strip())
            self.suspend   = flagSuspend
            self.override  = flagOverride
            if flagOverride is 1:
                self.target = targetOverride
        except:
            t.error = 'Error reading override file'

    def updateBounds(self, m):
        if m.ask > self.maxPrice:
            self.maxPrice = m.ask
            self.minPrice = self.maxPrice * (1 - self.walkDown)
        if m.bid < self.minPrice:
            self.minPrice = m.bid
            self.maxPrice = self.minPrice * (1 + self.walkUp)
        return self.minPrice, self.maxPrice

    def calcBaseWeight(self, marketData):
        minPrice = self.minPrice
        maxPrice = self.maxPrice
        p = (marketData.bid + marketData.ask)/2
        if marketData.bid < self.minPrice:
            self.target = self.backupFund
        elif marketData.ask > self.maxPrice:
            self.target = 1
        else:
            y = (p - minPrice)/(maxPrice - minPrice) * (1 - self.backupFund)
            self.target = self.backupFund + y
        return self.target

    def checkAllin(self, m, btFlag, emailAddress):
    #   If price is below cutoff, go all in 
        if m.price < m.high * (1 - self.allinLimit):
            if self.allinFlag == 0:
    #           print('Going all-in.')
                if btFlag != 1:
                    bbFunctions.sendEmail(self, emailAddress, 'Going all-in.')
            self.target = 0
            self.allinFlag = 1
        else:
            self.allinFlag = 0
        return self.target

    def calcMomentum(self, m):
        mom  = - (m.price/m.mean-1)
        self.target = self.target * (1 + self.momFactor * mom)
        return self.target

    def calcCoinsToTrade(self, m, p):
        if self.target == p.weight:
            self.tradePrice = 0
            self.coinsToTrade = 0
            return self.coinsToTrade
        elif self.target < p.weight:
            self.tradePrice = m.ask
        elif self.target > p.weight:
            self.tradePrice = m.bid
        N = self.target * (p.EUR + p.BTC * m.bid) - p.EUR
        D = self.target * (self.tradePrice - m.bid) - self.tradePrice
        try:
            self.coinsToTrade = N/D
        except ZeroDivisionError:
            self.coinsToTrade = 0
        return self.coinsToTrade

    def stopLoss(self, m, p, overrideFileName):
        if m.price < m.high * (1 - self.stopLossLimit):
            self.coinsToTrade = -p.BTC
            # Should recalculate bid price here!
            with open(overrideFileName, 'wt') as of:
                of.write('override = ' + str(1) + '\n')
                of.write('target   = ' + str(1) + '\n')
                of.write('suspend  = ' + str(0) + '\n')
            print('Trading frozen.')
            bbFunctions.sendEmail(self, emailAddress, 'Trading has been frozen.')
            return self.coinsToTrade


    def checkTradeSize(self, m, p, tradeFactor):
        if self.coinsToTrade < -p.BTC:
                self.coinsToTrade = -p.BTC
        if self.coinsToTrade > p.EUR / m.ask:
                self.coinsToTrade = p.EUR / m.ask
        minTrade = tradeFactor * p.value
        if abs(self.coinsToTrade) < minTrade:
            if self.target is not self.backupFund and self.target is not 1:
                self.coinsToTrade = 0
                return self.coinsToTrade
        if self.suspend == 1:
                self.coinsToTrade = 0
                return self.coinsToTrade
        return self.coinsToTrade
        
    def handle_error(self, m, emailAddress, errorFileName):
    #   print(self.error)
        with open(errorFileName, 'at') as ef:
            ef.write(m.time + '\t')
            ef.write(self.error + '\n')
        self.error = 0
