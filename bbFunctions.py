import linecache
import time
import sys
import re

def cancelOrders(krakenAPI):
    openOrders = krakenAPI.query_private('OpenOrders')['result']
    if openOrders['open'] != {}:
        for transaction in openOrders['open'].keys():
            krakenAPI.query_private('CancelOrder', {'txid':transaction})

def file_len(fname):
    with open(fname) as f:
        for i, l in enumerate(f):
            pass
    return i + 1

def getBounds(logFileName, walkUp, walkDown):
    with open(logFileName,'r') as logFile:
        history = logFile.readlines()
    maxPrice = float(re.split(',', history[1])[2])
    minPrice = float(re.split(',', history[1])[1])
    for line in range(2,len(history)):
        if float(re.split(',', history[line])[2]) > maxPrice:
            maxPrice = float(re.split(',', history[line])[2])
            minPrice = maxPrice * (1 - walkDown)
        if float(re.split(',', history[line])[1]) < minPrice:
            minPrice = float(re.split(',', history[line])[1])
            maxPrice = minPrice * (1 + walkUp)
    return minPrice, maxPrice

def getData(krakenAPI, p, m):
    m.time   = krakenAPI.query_public('Time')['result']['rfc1123'][5:20]
    tickData = krakenAPI.query_public('Ticker', {'pair' : 'XXBTZEUR'})
    balance  = krakenAPI.query_private('Balance')['result']
    m.bid = float(tickData['result']['XXBTZEUR']['b'][0])
    m.ask = float(tickData['result']['XXBTZEUR']['a'][0])
    p.EUR  = float(balance['ZEUR'])
    p.BTC  = float(balance['XXBT'])
    p.weight = p.EUR / (p.EUR + p.BTC * m.bid)

    return p, m

def getDataBacktest(logFile, m, p, i):
    data = re.split(',', linecache.getline(logFile, i+1))
    m.time = data[0]
    m.bid = float(data[1])
    m.ask = float(data[2])

    p.weight = p.EUR / (p.EUR + p.BTC * m.bid)

    return m, p

def placeOrder(krakenAPI, m, t):
    if t.coinsToTrade < 0:
        trade = krakenAPI.query_private('AddOrder', {
            'pair' : 'XXBTZEUR',
            'type' : 'sell', 
            'ordertype' : 'limit',
            'price' : m.ask, 
            'volume' : -t.coinsToTrade
        })
        t.error = 0
    else:
        trade = krakenAPI.query_private('AddOrder', {
            'pair' : 'XXBTZEUR',
            'type' : 'buy',
            'ordertype' : 'limit',
            'price' : m.bid,
            'volume' : t.coinsToTrade
         })
        t.error = 0
    if trade['error'] != []:
        t.error = 1

def printLogLine(p, m, t, logFileName):
    with open(logFileName,'a') as logFile:
        logFile.write(m.time + ',')
        logFile.write(str(m.bid) + ',')
        logFile.write(str(m.ask) + ',')
        logFile.write(str(p.EUR) + ',')
        logFile.write(str(p.BTC) + ',')
        logFile.write(str(t.coinsToTrade) + '\n')

def printTermLine(p, m, t):
    strLog = m.time
    strLog = strLog + ' | B: '+ '{0:>5.1f}'.format(m.bid) + ' A: '+ '{0:>5.1f}'.format(m.ask)
    strLog = strLog + ' | EUR: ' + '{0:>6.1f}'.format(p.EUR) + ' BTC: ' + '{0:>5.3f}'.format(p.BTC)
    strLog = strLog + ' | Bounds: ' + '{0:>5.1f}'.format(t.minPrice) + ' ' + '{0:>5.1f}'.format(t.maxPrice)
    strLog = strLog + ' | Trade: ' + '{0:>4.1f}'.format(t.coinsToTrade) 
    print(strLog)
    sys.stdout.flush()
    return 0
