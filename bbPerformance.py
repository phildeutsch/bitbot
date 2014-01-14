import pandas as pd
from math import isnan
import sys

def showPerformance(df, date, transfers=None):
    if transfers != None:
        w = pd.read_csv(transfers, parse_dates=[0], index_col=0)
    else:
        w = []
        
    if date != 'all':
        df = df[date]
        try:
            w = w[date]
        except:
            w = []

    startValue = float(df[:1]['EUR'] + df[:1]['BTC'] * df[:1]['Bid'])
    endValue   = float(df.tail(1)['EUR'] + df.tail(1)['BTC'] * df.tail(1)['Bid'])
    if len(w) != 0:
        endValue   = endValue + float(w.sum()['Amount'] * w.sum()['Bid'])
    retStrategy= endValue / startValue - 1

    btcHold   = float(startValue / df[:1]['Ask'])
    endHold   = float(btcHold * df.tail(1)['Bid'])
    if len(w) != 0:
        endHold   = endHold + float(w.sum()['Amount'] * w.sum()['Bid'])
    retHold   = endHold / startValue - 1 

    buys    = df['Trade'].map(lambda x: x > 0.01)
    sells   = df['Trade'].map(lambda x: x < -0.01)

    sellAmounts = df[sells].Trade * df[sells].Bid
    sellTotal   = df[sells].sum()['Trade']
    avgSellPrice= sellAmounts.sum() / sellTotal
    buyAmounts  = df[buys].Trade * df[buys].Ask
    buyTotal    = df[buys].sum()['Trade']
    avgBuyPrice = buyAmounts.sum() / buyTotal
    if isnan(avgBuyPrice):
        avgBuyPrice = 0
    if isnan(avgSellPrice):
        avgSellPrice = 0

    sys.stdout.write('{0:<10}'.format(date))
    sys.stdout.write('{0:>8.1f}'.format(float(buyTotal)))
    sys.stdout.write('{0:>8.1f}'.format(float(avgBuyPrice)))
    sys.stdout.write('{0:>8.1f}'.format(float(-sellTotal)))
    sys.stdout.write('{0:>8.1f}'.format(float(avgSellPrice)))
    sys.stdout.write(str('{0:>8.1f}'.format(float(100*retStrategy))) + '%')
    sys.stdout.write(str('{0:>8.1f}'.format(float(100*retHold)) + '%\n'))
    
    return [buyTotal, avgBuyPrice, sellTotal, avgSellPrice]

def makePerformanceTable(logFile, transfers=None):
    history = pd.read_csv(logFile, parse_dates=[0], index_col=0)
    dates=history.index.values
    uniqueDates = []
    for d in range(len(dates)):
        if str(dates[d])[0:10] not in uniqueDates:
            uniqueDates.append(str(dates[d])[0:10])
    sys.stdout.write('{0:<10}'.format('Date'))
    sys.stdout.write('{0:>8}'.format('Bought'))
    sys.stdout.write('{0:>8}'.format('Ask'))
    sys.stdout.write('{0:>8}'.format('Sold'))
    sys.stdout.write('{0:>8}'.format('Bid'))
    sys.stdout.write('{0:>9}'.format('Strategy'))
    sys.stdout.write('{0:>9}'.format('Buy&Hold'))
    print()
    showPerformance(history, 'all', transfers)
    for d in uniqueDates:
        showPerformance(history, d, transfers)

def getTotalPerformance(logFile):
    df = pd.read_csv(logFile, parse_dates=[0], index_col=0)
    startValue = float(df[:1]['EUR'] + df[:1]['BTC'] * df[:1]['Bid'])
    endValue   = float(df.tail(1)['EUR'] + df.tail(1)['BTC'] * df.tail(1)['Bid'])
    return endValue / startValue - 1
