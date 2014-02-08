from bbFunctions import *
from bbSettings import *
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
        self.mean = self.price
        self.histPrices = deque([], priceWindow)

class trader:
    """ Stores all trade parameters """
    buys  = deque([], priceWindow)
    sells = deque([], priceWindow)
    
    def __init__(self, logFileName, walkUp, walkDown, midDistance, tradeBuffer, priceWindow):
        self.maxPrice = 0
        self.minPrice = 0
        self.midPrice = 0
        self.tradeBuffer = tradeBuffer
        self.midDistance = midDistance
        self.walkUp = walkUp
        self.walkDown = walkDown
        self.midPrice = self.minPrice + \
            self.midDistance * (self.maxPrice - self.minPrice)
        self.coinsToTrade = 0
        self.target = 0
        self.tradePrice = 1
        self.freeze = False

    def updateBounds(self, m):
        if m.ask > self.maxPrice:
            self.maxPrice = m.ask
            self.minPrice = self.maxPrice * (1 - self.walkDown)
        if m.bid < self.minPrice:
            self.minPrice = m.bid
            self.maxPrice = self.minPrice * (1 + self.walkUp)
        self.midPrice = self.minPrice + \
                        self.midDistance * (self.maxPrice - self.minPrice)
        return self.minPrice, self.maxPrice

    def calcBaseWeight(self, marketData):
        tb = self.tradeBuffer
        md = self.midDistance
        minPrice = self.minPrice
        maxPrice = self.maxPrice
        midPrice = self.midPrice
        p = (marketData.bid + marketData.ask)/2
        if minPrice == midPrice or midPrice == maxPrice:
            self.target = 1
            return self.target
        if marketData.bid < self.minPrice:
            self.target = tb
        elif marketData.ask > self.maxPrice:
            self.target = tb + (1-tb)/(1+tb)
        else:
    #       Linear
    #       y = tb + (p - minPrice)/(maxPrice - minPrice) * (1-tb)/(1+tb)
    #       Piecewise linear
            if p < midPrice:
                y = (1-md) * (p-minPrice)/(midPrice-minPrice)
            else:
                y = (1-md) + (p-midPrice)/(maxPrice-midPrice) * md
            y = tb + y * (1-tb)/(1+tb)
            self.target = y
        return self.target

    def calcMomentum(self, momFactor, m):
        try:
            mom  = - (m.price/m.mean-1)
        except ZeroDivisionError:
            mom  = 0
        self.target = self.target * (1 + momFactor * mom)
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

    def checkTradeSize(self, m, p, tradeFactor):
        if self.freeze is True:
            self.coinsToTrade = -p.BTC
            print('Trade suspended.')
            return self.coinsToTrade

        minTrade = tradeFactor * p.value
        if self.coinsToTrade < -p.BTC:
                self.coinsToTrade = -p.BTC
        if self.coinsToTrade > p.EUR / m.ask:
                self.coinsToTrade = p.EUR / m.ask
        if abs(self.coinsToTrade) < minTrade \
           or self.target is 0 \
           or self.target is 1:
            self.coinsToTrade = 0
            self.buys.append('null')
            self.sells.append('null')
            return 0
        elif self.coinsToTrade > minTrade:
            self.buys.append(m.ask)
            self.sells.append('null')
        elif self.coinsToTrade < -minTrade:
            self.buys.append('null')
            self.sells.append(m.bid)
        return self
