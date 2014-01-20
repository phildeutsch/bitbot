import pandas as pd
import numpy as np
from math import isnan
import sys

def showPerformance(df, tdf=[], date='Total'):
    if date != 'Total':
        df = df[date]
        try:
            tdf = tdf[date]
        except:
            tdf = []

    startValue = float(df[:1]['EUR'] + df[:1]['BTC'] * df[:1]['Bid'])
    endValue   = float(df.tail(1)['EUR'] + df.tail(1)['BTC'] * df.tail(1)['Bid'])
    if len(tdf) != 0:
        tdf['EUR']=tdf['Amount']*tdf['Bid']
        endValue   = endValue - float(tdf.sum()['EUR'])
    retStrategy= endValue / startValue - 1

    btcHold   = float(startValue / df[:1]['Ask'])
    endHold   = float(btcHold * df.tail(1)['Bid'])
    retHold   = endHold / startValue - 1 

#    buys    = df['Trade'].map(lambda x: x > 0.01)
#    sells   = df['Trade'].map(lambda x: x < -0.01)

#    sellAmounts = df[sells].Trade * df[sells].Bid
#    sellTotal   = df[sells].sum()['Trade']
#    avgSellPrice= sellAmounts.sum() / sellTotal
#    buyAmounts  = df[buys].Trade * df[buys].Ask
#    buyTotal    = df[buys].sum()['Trade']
#    avgBuyPrice = buyAmounts.sum() / buyTotal
#    if isnan(avgBuyPrice):
#        avgBuyPrice = 0
#    if isnan(avgSellPrice):
#        avgSellPrice = 0

    openPrice  = float((df[:1]['Bid'] + df[:1]['Ask'])/2)
    closePrice = float((df.tail(1)['Bid'] + df.tail(1)['Ask'])/2)    

    sys.stdout.write('{0:<10}'.format(date))
    sys.stdout.write('{0:>8.1f}'.format(float(openPrice)))
    sys.stdout.write('{0:>8.1f}'.format(float(closePrice)))
    sys.stdout.write(str('{0:>8.1f}'.format(float(100*retStrategy))) + '%')
    sys.stdout.write(str('{0:>8.1f}'.format(float(100*retHold)) + '%\n'))

    return retStrategy, retHold

def makePerformanceTable(logFile, start=None, end=None, transfers=None):
    history = pd.read_csv(logFile, parse_dates=[0], index_col=0)
    if transfers is None:
        t = []
    else:
        t = pd.read_csv(transfers, parse_dates=[0], index_col=0)
    if start is None:
        npstart = None
    else:
        npstart = np.datetime64(start)
    if end is None:
        npend = None
    else: npend = np.datetime64(end)
    history = history[npstart:npend]
    t = t[npstart:npend]
    dates=history.index.values
    uniqueDates = []
    for d in range(len(dates)):
        if str(dates[d])[0:10] not in uniqueDates:
            uniqueDates.append(str(dates[d])[0:10])
    sys.stdout.write('{0:<10}'.format('Date'))
    sys.stdout.write('{0:>8}'.format('Open'))
    sys.stdout.write('{0:>8}'.format('Close'))
    sys.stdout.write('{0:>9}'.format('Strategy'))
    sys.stdout.write('{0:>10}'.format('Buy&Hold\n'))
    results = []
    for d in uniqueDates:
        results.append(showPerformance(history, t, d))
    showPerformance(history, t, 'Total')
    results = np.array(results)
#    np.set_printoptions(precision=4, suppress=True)
#    print(results)
    sys.stdout.write('{0:<26}'.format('Mean daily return:'))
    sys.stdout.write('{0:>8.1}'.format(float(results.mean(axis=0)[0])) + '%')    
    sys.stdout.write('{0:>8.1}'.format(float(results.mean(axis=0)[1])) + '%\n')    
    sys.stdout.write('{0:<26}'.format('Mean daily std deviaton:'))
    sys.stdout.write('{0:>8.1}'.format(float(results.std(axis=0)[0])) + '%')    
    sys.stdout.write('{0:>8.1}'.format(float(results.std(axis=0)[1])) + '%\n')    
    print('')

def getTotalPerformance(logFile):
    df = pd.read_csv(logFile, parse_dates=[0], index_col=0)
    startValue = float(df[:1]['EUR'] + df[:1]['BTC'] * df[:1]['Bid'])
    endValue   = float(df.tail(1)['EUR'] + df.tail(1)['BTC'] * df.tail(1)['Bid'])
    return endValue / startValue - 1
