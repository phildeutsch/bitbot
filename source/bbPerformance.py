import pandas as pd
import numpy as np
from math import isnan, sqrt
import sys

def drawdown(r):
    prices = np.ones(len(r)+1)
    prices[0] = 100
    for i in range(1,len(prices)):
        prices[i] = prices[i-1] * (1 + r[i-1])
    
    prevmaxi = 0
    prevmini = 0
    maxi = 0

    for i in range(len(prices))[1:]:
        if prices[i] >= prices[maxi]:
            maxi = i
        else:
        # You can only determine the largest drawdown on a downward price!
            if (prices[maxi] - prices[i]) > (prices[prevmaxi] - prices[prevmini]):
                prevmaxi = maxi
                prevmini = i
    low = prices[prevmini]
    high = prices[prevmaxi]
    return low/high - 1
    
def sortino(r):
    avgReturn = r.mean()
    avgNegVol = r[r<0].std()
    return avgReturn / avgNegVol * sqrt(365)
    
def sharpe(r):
    avgReturn = r.mean()
    avgVol    = r.std()
    return avgReturn / avgVol * sqrt(365)
    
def totalReturn(r):
    t = 1
    for i in range(len(r)):
        t *= (1 + r[i])
    return (t-1)
 
def calcReturn(log, transactions, date):
    startt = str(np.datetime64(date + 'T00:01'))[:16]
    endt   = str(np.datetime64(date + 'T23:59'))[:16]
    starty = str(np.datetime64(date + 'T00:01') - np.timedelta64(1, 'D'))[:16]
    endy   = str(np.datetime64(date + 'T23:59') - np.timedelta64(1, 'D'))[:16]

    dft = log[startt : endt]
    dfy = log[starty : endy]

    try:
        tdf = transactions[date]
    except:
        tdf = []

    if len(dfy) > 0:
        startValue = float(dfy.tail(1)['EUR'] + \
                           dfy.tail(1)['BTC'] * dfy.tail(1)['Bid'])
        openPrice  = float((dfy.tail(1)['Bid'] + dfy.tail(1)['Ask'])/2)
    else:
        startValue = float(dft.head(1)['EUR'] + \
                           dft.head(1)['BTC'] * dft.head(1)['Bid'])
        openPrice  = float((dft.head(1)['Bid'] + dft.head(1)['Ask'])/2)
        
    endValue   = float(dft.tail(1)['EUR'] + \
                       dft.tail(1)['BTC'] * dft.tail(1)['Bid'])
    closePrice = float((dft.tail(1)['Bid'] + dft.tail(1)['Ask'])/2)
    
    if len(tdf) != 0:
        tdf['EUR']=tdf['AmountBTC']*(tdf['Bid']+tdf['Ask'])/2 + tdf['AmountEUR']
        endValue   = endValue - float(tdf.sum()['EUR'])
    
    retStrategy= endValue / startValue - 1
    retHold    = closePrice / openPrice - 1
    return openPrice, closePrice, retHold, retStrategy

def getReturns(logFileName, transfers=None, start=None, end=None):
    history   = pd.read_csv(logFileName, parse_dates=[0], index_col=0)
 
    if start is None:
        start = '2014-01-08'
        npstart = np.datetime64(start + 'T23:50') - np.timedelta64(1, 'D')
        npstart = str(npstart)[:16]
    else:
        npstart = start + ' 23:50'
        npstart = np.datetime64(start + 'T23:50') - np.timedelta64(1, 'D')
        npstart = str(npstart)[:16]
    if end is None:
        npend = None
    else: 
        npend = np.datetime64(end + 'T23:59')
        npend = str(npend)[:16]
    print(npstart, npend)
    history     = history[npstart:npend]
 
    if transfers is None:
        t = []
    else:
        t = pd.read_csv(transfers, parse_dates=[0], index_col=0)
        t = t[npstart:npend]

    dates       = history.index.values
    uniqueDates = []
    r = []
    for d in range(len(dates)):
        if str(dates[d])[0:10] not in uniqueDates:
            uniqueDates.append(str(dates[d])[0:10])
    if uniqueDates[0] != start:
        uniqueDates = uniqueDates[1:]
    if end is not None and uniqueDates[-1] != end:
        uniqueDates = uniqueDates[:-1]
    for d in uniqueDates:
            r.append(calcReturn(history, t, d))
    return uniqueDates, np.array(r)

def printReturns(dates, returns):
    sys.stdout.write('{0:<10}'.format('Date'))
    sys.stdout.write('{0:>8}'.format('Open'))
    sys.stdout.write('{0:>8}'.format('Close'))
    sys.stdout.write('{0:>9}'.format('Buy&Hold'))
    sys.stdout.write('{0:>10}'.format('Strategy'))
    sys.stdout.write('\n')
    for d in range(len(dates)):
        sys.stdout.write('{0:<10}'.format(dates[d]))
        sys.stdout.write('{0:>8.1f}'.format(returns[d][0]))
        sys.stdout.write('{0:>8.1f}'.format(returns[d][1]))
        sys.stdout.write('{0:>8.2f}'.format(100*returns[d][2]) + '%')
        sys.stdout.write('{0:>8.2f}'.format(100*returns[d][3]) + '%')
        sys.stdout.write('\n')

def printSummary(returns):
    sys.stdout.write('{0:<26}'.format('Total return:'))
    sys.stdout.write('{0:>8.2f}'.format(100*totalReturn(returns[:,2])) + '%')    
    sys.stdout.write('{0:>8.2f}'.format(100*totalReturn(returns[:,3])) + '%')
    sys.stdout.write('\n')
    
    sys.stdout.write('{0:<26}'.format('Average return:'))
    sys.stdout.write('{0:>8.2f}'.format(returns[:,2].mean()) + '%')    
    sys.stdout.write('{0:>8.2f}'.format(returns[:,3].mean()) + '%')
    sys.stdout.write('\n')
    
    sys.stdout.write('{0:<26}'.format('Sharpe ratio:'))
    sys.stdout.write('{0:>8.2f}'.format(sharpe(returns[:,2])))    
    sys.stdout.write('{0:>9.2f}'.format(sharpe(returns[:,3])))
    sys.stdout.write('\n')
    
    sys.stdout.write('{0:<26}'.format('Sortino ratio:'))
    sys.stdout.write('{0:>8.2f}'.format(sortino(returns[:,2])))    
    sys.stdout.write('{0:>9.2f}'.format(sortino(returns[:,3])))
    sys.stdout.write('\n')
    
    sys.stdout.write('{0:<26}'.format('Maximum drawdown:'))
    sys.stdout.write('{0:>8.2f}'.format(100*drawdown(returns[:,2])) + '%')    
    sys.stdout.write('{0:>8.2f}'.format(100*drawdown(returns[:,3])) + '%')
    sys.stdout.write('\n')
