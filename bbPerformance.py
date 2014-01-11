import pandas as pd
import sys

def showPerformance(df, date):
    w = pd.read_csv(transferFile, parse_dates=[0], index_col=0)
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
    
    sys.stdout.write(date)
    if len(date) < 10:
        sys.stdout.write('\t')
    sys.stdout.write('\t' + str(round(buyTotal,3)))
    sys.stdout.write('\t' + str(round(avgBuyPrice,1)))
    sys.stdout.write('\t\t' + str(round(-sellTotal,3)))
    sys.stdout.write('\t' + str(round(avgSellPrice,1)))
    sys.stdout.write('\t\t' + str(round(100*retStrategy,1)) + '%')
    sys.stdout.write('\t' + str(round(100*retHold,1)) + '%\n')
    

    return [buyTotal, avgBuyPrice, sellTotal, avgSellPrice]

def makePerformanceTable(logFile):
    history = pd.read_csv(logFile, parse_dates=[0], index_col=0)
    dates=history.index.values
    uniqueDates = []
    for d in range(len(dates)):
        if str(dates[d])[0:10] not in uniqueDates:
            uniqueDates.append(str(dates[d])[0:10])
    print 'Date \t\tBought \tBuy Price \tSold \tSell Price \tReturn \tBuy&Hold' 
    showPerformance(history, 'all')
    for d in uniqueDates:
        showPerformance(history, d)

def getTotalPerformance(logFile):
    df = pd.read_csv(logFile, parse_dates=[0], index_col=0)
    startValue = float(df[:1]['EUR'] + df[:1]['BTC'] * df[:1]['Bid'])
    endValue   = float(df.tail(1)['EUR'] + df.tail(1)['BTC'] * df.tail(1)['Bid'])
    return endValue / startValue - 1

    
  

