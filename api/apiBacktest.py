import time
import datetime
import linecache 
import re
 
class API(object):
    """
    Used for backtesting 
     
    """
     
    def __init__(self, logFileName):
        self.logFileName = logFileName
        self.line = 1
 
		
    def getPrices(self, m, coinsToTrade=None):
        data = re.split(',', linecache.getline(self.logFileName, self.line+1))
        m.time = data[0]
        m.bid = float(data[1])
        m.ask = float(data[2])
        m.price = (m.bid + m.ask)/2
        m.histPrices.append(m.price)
        m.mean = sum(m.histPrices)/len(m.histPrices)
        self.line += 1
        
        if m.bid < m.low:
            m.low = m.bid
        if m.ask > m.high:
            m.high = m.bid
            
        return m.bid, m.ask
        
    def getBalance(self, m, p, t):
        p.BTC = p.BTC + t.coinsToTrade
        if t.coinsToTrade > 0:
            p.EUR = p.EUR - t.coinsToTrade * m.ask
        elif t.coinsToTrade < 0:
            p.EUR = p.EUR - t.coinsToTrade * m.bid

        p.value = p.EUR + p.BTC * m.bid
        p.weight = p.EUR / p.value
        t.minTrade = t.tradeFactor * p.value
        return p.value
