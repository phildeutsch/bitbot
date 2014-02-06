import pandas as pd
import numpy as np
from math import isnan, sqrt
import sys

def drawdown(r):
    prices = np.ones(len(r))
    prices[0] = 100
    for i in range(1,len(r)):
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
    return 100 * (low/high - 1)

def showPerformance(df, bt=None, tdf=[], date='Total'):
    if date != 'Total':
        dft = df[np.datetime64(date + 'T00:01') : np.datetime64(date + 'T23:59')]
        dfy = df[np.datetime64(date + 'T00:01') - np.timedelta64(1, 'D') : \
                 np.datetime64(date + 'T23:59') - np.timedelta64(1, 'D')]
        try:
            tdf = tdf[date]
        except:
            tdf = []

        startValue = float(dfy.tail(1)['EUR'] + \
                           dfy.tail(1)['BTC'] * dfy.tail(1)['Bid'])
        endValue   = float(dft.tail(1)['EUR'] + \
                           dft.tail(1)['BTC'] * dft.tail(1)['Bid'])
        openPrice  = float((dfy.tail(1)['Bid'] + dfy.tail(1)['Ask'])/2)
        closePrice = float((dft.tail(1)['Bid'] + dft.tail(1)['Ask'])/2)
        if bt is not None:
            btt = bt[np.datetime64(date + 'T00:01') : np.datetime64(date + 'T23:59')]
            bty = bt[np.datetime64(date + 'T00:01') - np.timedelta64(1, 'D') : \
                     np.datetime64(date + 'T23:59') - np.timedelta64(1, 'D')]
            startValBT = float(bty.tail(1)['EUR'] + \
                               bty.tail(1)['BTC'] * bty.tail(1)['Bid'])
            endValBT   = float(btt.tail(1)['EUR'] + \
                               btt.tail(1)['BTC'] * btt.tail(1)['Bid'])
            retBT = endValBT / startValBT - 1
    else:
        npstart = np.datetime64(str(df.head(1).index.values)[2:12] + 'T23:50')
        df = df[npstart:]
        if bt is not None:
            bt = bt[npstart:]
        try:
            tdf = tdf[npstart:]
        except:
            tdf = []

        startValue = float(df.head(1)['EUR'] + \
                           df.head(1)['BTC'] * df.head(1)['Bid'])
        endValue   = float(df.tail(1)['EUR'] + \
                           df.tail(1)['BTC'] * df.tail(1)['Bid'])
        openPrice  = float((df.head(1)['Bid'] + df.head(1)['Ask'])/2)
        closePrice = float((df.tail(1)['Bid'] + df.tail(1)['Ask'])/2)
        if bt is not None:
            startValBT = float(bt.head(1)['EUR'] + \
                               bt.head(1)['BTC'] * bt.head(1)['Bid'])
            endValBT   = float(bt.tail(1)['EUR'] + \
                               bt.tail(1)['BTC'] * bt.tail(1)['Bid'])
            retBT = endValBT / startValBT - 1
                                
    if len(tdf) != 0:
        tdf['EUR']=tdf['Amount']*tdf['Bid']
        endValue   = endValue - float(tdf.sum()['EUR'])
    retStrategy= endValue / startValue - 1
    retHold    = closePrice / openPrice - 1

    sys.stdout.write('{0:<10}'.format(date))
    sys.stdout.write('{0:>8.2f}'.format(float(openPrice)))
    sys.stdout.write('{0:>8.2f}'.format(float(closePrice)))
    sys.stdout.write(str('{0:>8.2f}'.format(float(100*retHold))) + '%')
    sys.stdout.write(str('{0:>8.2f}'.format(float(100*retStrategy))) + '%')
    if bt is not None:
        sys.stdout.write(str('{0:>8.2f}'.format(float(100*retBT)) + '%\n'))
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
        npstart = np.datetime64(start + 'T23:50') - np.timedelta64(1, 'D')
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
    for d in uniqueDates[1:]:
        results.append(showPerformance(history, historyBT, t, d))
    
    showPerformance(history, historyBT, t, 'Total')
    results = np.array(results)

#    np.set_printoptions(precision=4, suppress=True)
#    print(results)
    print('')
    rbh = float(100*results.mean(axis=0)[0])
    rst = float(100*results.mean(axis=0)[1])
    sbh = float(100*results.std(axis=0)[0])
    sst = float(100*results.std(axis=0)[1])
    dbh = float(100*results[:,0][results[:,0]<0].std())
    dst = float(100*results[:,1][results[:,1]<0].std())
    if logFileNameBT is not None:
        rbt = float(100*results.mean(axis=0)[2])
        sbt = float(100*results.std(axis=0)[2])
        dbt = float(100*results[:,2][results[:,2]<0].std())

    sys.stdout.write('{0:<26}'.format('Mean daily return:'))
    sys.stdout.write('{0:>8.2f}'.format(rbh) + '%')    
    sys.stdout.write('{0:>8.2f}'.format(rst) + '%')    
    if logFileNameBT is not None:
        sys.stdout.write('{0:>8.2f}'.format(float(results.mean(axis=0)[2])) + '%\n')    
    else:
        sys.stdout.write('\n')
    sys.stdout.write('{0:<26}'.format('Mean daily std deviaton:'))
    sys.stdout.write('{0:>8.2f}'.format(sbh) + '%')    
    sys.stdout.write('{0:>8.2f}'.format(sst) + '%')     
    if logFileNameBT is not None:
        sys.stdout.write('{0:>8.2f}'.format(float(results.std(axis=0)[2])) + '%\n')    
    else:
        sys.stdout.write('\n')
    sys.stdout.write('{0:<26}'.format('Annualized Sharpe ratio:'))
    sys.stdout.write('{0:>8.2f}'.format(rbh/sbh * sqrt(365)))    
    sys.stdout.write('{0:>9.2f}'.format(rst/sst * sqrt(365)))
    if logFileNameBT is not None:
        sys.stdout.write('{0:>9.2f}'.format(rbt/sbt * sqrt(365)) + '\n')
    else:
        sys.stdout.write('\n')
    sys.stdout.write('{0:<26}'.format('Annualized Sortino ratio:'))
    sys.stdout.write('{0:>8.2f}'.format(rbh/dbh * sqrt(365)))    
    sys.stdout.write('{0:>9.2f}'.format(rst/dst * sqrt(365)))
    if logFileNameBT is not None:
        sys.stdout.write('{0:>9.2f}'.format(rbt/dbt * sqrt(365)) + '\n')
    else:
        sys.stdout.write('\n')
    sys.stdout.write('{0:<26}'.format('Maximum drawdown:'))
    sys.stdout.write('{0:>8.2f}'.format(drawdown(results[:,0])) + '%')    
    sys.stdout.write('{0:>8.2f}'.format(drawdown(results[:,1])) + '%')
    if logFileNameBT is not None:
        sys.stdout.write('{0:>8.2f}'.format(drawdown(results[:,2])) + '%\n')
    else:
        sys.stdout.write('\n')  
    print('')
    if logFileNameBT is not None:
        return rbh, sbh, rst, sst, rbt, sbt
    return rbh, sbh, rst, sst

def getTransactions(logFileName, transFileName):
    history  = pd.read_csv(logFileName, parse_dates=[0], index_col=0)
    df  = history.diff()    
    tx  = (df['Trade'] == 0) & (df['BTC'] != 0) & (df['EUR'] == 0)
    amounts = df[tx]['BTC']
    out = history.loc[amounts.index.values,:].loc[:,['Bid','Ask']]
    out['Amount'] = amounts
    out.to_csv(transFileName)     
