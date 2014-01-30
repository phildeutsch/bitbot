import pandas as pd
import numpy as np
from math import isnan
import sys

def showPerformance(df, bt=None, tdf=[], date='Total'):
    if date != 'Total':
        df = df[date]
        if bt is not None:
            bt = bt[date]
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
    if bt is not None:
        endValBT   = float(bt.tail(1)['EUR'] + bt.tail(1)['BTC'] * bt.tail(1)['Bid'])
        startValBT = float(bt[:1]['EUR'] + bt[:1]['BTC'] * bt[:1]['Bid'])
        retBT = endValBT / startValBT - 1
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

    retHold    = closePrice / openPrice - 1

    sys.stdout.write('{0:<10}'.format(date))
    sys.stdout.write('{0:>8.1f}'.format(float(openPrice)))
    sys.stdout.write('{0:>8.1f}'.format(float(closePrice)))
    sys.stdout.write(str('{0:>8.1f}'.format(float(100*retHold))) + '%')
    sys.stdout.write(str('{0:>8.1f}'.format(float(100*retStrategy))) + '%')
    if bt is not None:
        sys.stdout.write(str('{0:>8.1f}'.format(float(100*retBT)) + '%\n'))
        return retHold, retStrategy, retBT
    else:
        sys.stdout.write('\n')
        return retHold, retStrategy

def makePerformanceTable(logFileName, logFileNameBT=None, start=None, end=None, transfers=None):
    history   = pd.read_csv(logFileName, parse_dates=[0], index_col=0)
    if logFileNameBT is not None:
        historyBT = pd.read_csv(logFileNameBT, parse_dates=[0], index_col=0)
    else:
        historyBT = None
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
    else: 
        npend = np.datetime64(end + 'T23:59')
    history     = history[npstart:npend]
    if logFileNameBT is not None:
        historyBT   = historyBT[npstart:npend]
    t           = t[npstart:npend]
    dates       = history.index.values
    uniqueDates = []
    for d in range(len(dates)):
        if str(dates[d])[0:10] not in uniqueDates:
            uniqueDates.append(str(dates[d])[0:10])
    sys.stdout.write('{0:<10}'.format('Date'))
    sys.stdout.write('{0:>8}'.format('Open'))
    sys.stdout.write('{0:>8}'.format('Close'))
    sys.stdout.write('{0:>9}'.format('Buy&Hold'))
    sys.stdout.write('{0:>10}'.format('Strategy'))
    if logFileNameBT is not None:
        sys.stdout.write('{0:>10}'.format('Backtest\n'))
    else:
        sys.stdout.write('\n')
    results = []
    for d in uniqueDates:
        results.append(showPerformance(history, historyBT, t, d))
    showPerformance(history, historyBT, t, 'Total')
    results = np.array(results)
#    np.set_printoptions(precision=4, suppress=True)
#    print(results)
    sys.stdout.write('{0:<26}'.format('Mean daily return:'))
    sys.stdout.write('{0:>8.1}'.format(float(results.mean(axis=0)[0])) + '%')    
    sys.stdout.write('{0:>8.1}'.format(float(results.mean(axis=0)[1])) + '%')    
    if logFileNameBT is not None:
        sys.stdout.write('{0:>8.1}'.format(float(results.mean(axis=0)[2])) + '%\n')    
    else:
        sys.stdout.write('\n')
    sys.stdout.write('{0:<26}'.format('Mean daily std deviaton:'))
    sys.stdout.write('{0:>8.1}'.format(float(results.std(axis=0)[0])) + '%')    
    sys.stdout.write('{0:>8.1}'.format(float(results.std(axis=0)[1])) + '%')     
    if logFileNameBT is not None:
        sys.stdout.write('{0:>8.1}'.format(float(results.std(axis=0)[2])) + '%\n')    
    else:
        sys.stdout.write('\n')
    print('')

def getTransactions(logFileName, transFileName):
    history  = pd.read_csv(logFileName, parse_dates=[0], index_col=0)
    df  = history.diff()    
    tx  = (df['Trade'] == 0) & (df['BTC'] != 0) & (df['EUR'] == 0)
    amounts = df[tx]['BTC']
    out = history.loc[amounts.index.values,:].loc[:,['Bid','Ask']]
    out['Amount'] = amounts
    out.to_csv(transFileName)     
