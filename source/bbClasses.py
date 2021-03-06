import bbCfg
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

    def __init__(self, time, bid, ask):
        self.time = time
        self.bid = bid
        self.ask = ask
        self.price = (bid + ask)/2
        self.histPrices = deque([], int(bbCfg.priceWindow))
        self.mean = self.price
        self.low = self.price
        self.high = self.price

class trader:
    """ Stores all trade parameters """
    
    def __init__(self, logFileName):
        try:
            self.minPrice, self.maxPrice = bbFunctions.getBounds(logFileName, 
                                           bbCfg.walkUp, bbCfg.walkDown)
        except:
            self.minPrice = 0
            self.maxPrice = 0
        self.coinsToTrade = 0
        self.target = 1
        self.tradePrice = 1
        self.override = 0
        self.suspend = 0
        self.minTrade = 0
        self.allinFlag = 0
        self.buys  = deque([], bbCfg.priceWindow)
        self.sells = deque([], bbCfg.priceWindow)
        self.error = 0

    def checkOverride(self):
        try:
            with open(bbCfg.overrideFileName, 'rt') as of:
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
            self.minPrice = self.maxPrice * (1 - bbCfg.walkDown)
        if m.bid < self.minPrice:
            self.minPrice = m.bid
            self.maxPrice = self.minPrice * (1 + bbCfg.walkUp)
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
            y = (p - minPrice)/(maxPrice - minPrice) * (1 - bbCfg.backupFund)
            self.target = bbCfg.backupFund + y
        return self.target

    def checkAllin(self, m, btFlag):
    #   If price is below cutoff, go all in 
        if m.price < m.high * (1 - bbCfg.allinLimit):
            if self.allinFlag == 0:
    #           print('Going all-in.')
                if btFlag != 1:
                    bbFunctions.sendEmail(self, bbCfg.emailAddress, 'Going all-in.')
            self.target = 0
            self.allinFlag = 1
        elif m.price > 1.01 * m.high * (1 - bbCfg.allinLimit):
            self.allinFlag = 0
        return self.target

    def calcMomentum(self, m):
        mom  = - (m.price/m.mean-1)
        self.target = self.target * (1 + bbCfg.momFactor * mom)
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

    def stopLoss(self, m, p):
        if m.price < m.high * (1 - bbCfg.stopLossLimit):
            self.coinsToTrade = -p.BTC
            # Should recalculate bid price here!
            with open(bbCfg.overrideFileName, 'wt') as of:
                of.write('override = ' + str(1) + '\n')
                of.write('target   = ' + str(1) + '\n')
                of.write('suspend  = ' + str(0) + '\n')
            print('Trading frozen.')
            bbFunctions.sendEmail(self, bbCfg.emailAddress, 'Trading has been frozen.')
            return self.coinsToTrade


    def checkTradeSize(self, m, p):
        if self.coinsToTrade < -p.BTC:
                self.coinsToTrade = -p.BTC
        if self.coinsToTrade > p.EUR / m.ask:
                self.coinsToTrade = p.EUR / m.ask
        minTrade = bbCfg.tradeFactor * p.value
        if abs(self.coinsToTrade) < minTrade:
            if self.target is not bbCfg.backupFund and self.target is not 1:
                self.coinsToTrade = 0
                return self.coinsToTrade
        if self.suspend == 1:
                self.coinsToTrade = 0
                return self.coinsToTrade
        return self.coinsToTrade
        
    def handle_error(self, m):
    #   print(self.error)
        with open(bbCfg.errorFileName, 'at') as ef:
            ef.write(m.time + '\t')
            ef.write(self.error + '\n')
        self.error = 0
