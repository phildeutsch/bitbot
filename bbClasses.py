from bbSettings import *
from bbFunctions import *

class portfolio:
    """ Stores portfolio with holdings in EUR and BTC """
    def __init__(self, amountEUR, amountBTC):
        self.EUR = amountEUR
        self.BTC = amountBTC
        self.weight = 1

class marketData:
    """ Stores market data """
    def __init__(self, time, bid, ask):
        self.time = time
        self.bid = bid
        self.ask = ask
        self.mean = (bid + ask)/2


class trader:
    """ Stores all self parameters """
    def __init__(self, logFileName):
        try:
            self.maxPrice = getHistoricMax(logFileName)
            self.tradeBuffer = tradeBuffer
            self.midDistance = midDistance
            self.maxWalk = maxWalk
            self.minPrice = self.maxPrice * (1 - self.maxWalk)
            self.midPrice = self.minPrice + \
                self.midDistance * (self.maxPrice - self.minPrice)
        except IndexError:
            self.maxPrice = 0
            self.tradeBuffer = tradeBuffer
            self.midDistance = midDistance
            self.maxWalk = maxWalk
            self.minPrice = 0
            self.midPrice = 0
            self.coinsToTrade = 0
            self.target = 0

    def calcBaseWeight(self, marketData):
        tb = self.tradeBuffer
        md = self.midDistance
        minPrice = self.minPrice
        maxPrice = self.maxPrice
        midPrice = self.midPrice
        p = (marketData.bid + marketData.ask)/2
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

    def calcmomentum(self, m):
        price = (m.bid + m.ask)/2
        try:
            mom  = - (price/m.mean-1)
        except zerodivisionerror:
            mom  = 1
        self.target = self.target * mom
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
        self.coinsToTrade = N/D
        return self.coinsToTrade

    def checkTradeSize(self):
        if abs(self.coinsToTrade) < 0.5:
            self.coinsToTrade = 0
        return self.coinsToTrade
        
