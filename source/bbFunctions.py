import linecache
import time
import sys
import re

def cancelOrders(krakenAPI, t):
    try:
        openOrders = krakenAPI.query_private('OpenOrders')['result']
        if openOrders['open'] != {}:
            for transaction in openOrders['open'].keys():
                krakenAPI.query_private('CancelOrder', {'txid':transaction})
    except:
        t.error = 0    

def drawPlot(plotFileHead, plotFileTail, m, t):
    with open('Analysis/plot.html','w') as picFile:
        with open(plotFileHead,'rt') as file1:
            content = file1.readlines()
            picFile.write(''.join(content))

        for i in range(len(m.histPrices)):
            picFile.write('[' + str(i) + ',')
            picFile.write(str(m.histPrices[i]) + ',')
            picFile.write(str(t.buys[i]) + ',')
            picFile.write(str(t.sells[i]) + '],\n')

        with open(plotFileTail,'rt') as file2:
            content = file2.readlines()
            picFile.write(''.join(content))

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

def getData(krakenAPI, p, m, t):
    try:
        m.time   = krakenAPI.query_public('Time')['result']['rfc1123'][5:20]
        tickData = krakenAPI.query_public('Ticker', {'pair' : 'XXBTZEUR'})
        balance  = krakenAPI.query_private('Balance')['result']
        m.bid = float(tickData['result']['XXBTZEUR']['b'][0])
        m.ask = float(tickData['result']['XXBTZEUR']['a'][0])
        p.EUR  = float(balance['ZEUR'])
        p.BTC  = float(balance['XXBT'])
        p.value = p.EUR + p.BTC * m.bid
        p.weight = p.EUR / p.value
        m.price = (m.bid+m.ask)/2
        m.histPrices.append(m.price)
        m.mean = sum(m.histPrices)/len(m.histPrices)
    except:
        t.error = 0

    return p, m

def getDataBacktest(logFile,  m, p, t, i):
    data = re.split(',', linecache.getline(logFile, i+1))
    m.time = data[0]
    m.bid = float(data[1])
    m.ask = float(data[2])
    
    p.value = p.EUR + p.BTC * m.bid
    p.weight = p.EUR / p.value
    m.price = (m.bid+m.ask)/2
    m.histPrices.append(m.price)
    m.mean = sum(m.histPrices)/len(m.histPrices)

    return m, p

def placeOrder(krakenAPI, m, t):
    try:
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
    except:
        t.error = 1

def printLogLine(p, m, t, logFileName, bounds=0):
    with open(logFileName,'a') as logFile:
        logFile.write(m.time + ',')
        logFile.write(str(m.bid) + ',')
        logFile.write(str(m.ask) + ',')
        logFile.write(str(p.EUR) + ',')
        logFile.write(str(p.BTC) + ',')
        logFile.write(str(t.coinsToTrade))
        if bounds is 1:
            logFile.write(',' + str(t.minPrice))
            logFile.write(',' + str(t.maxPrice))
        logFile.write('\n')

def printStatus(p, m, t, statusFileName):
    with open(statusFileName, 'w') as statusFile:
        statusFile.write('{0:<10}'.format('Time:'))
        statusFile.write('{0:<10}'.format(m.time) + '\n')
        statusFile.write('{0:<10}'.format('Value:'))
        statusFile.write('{0:>7.7f}'.format(p.EUR + p.BTC * m.bid) + '\n')
        statusFile.write('{0:<10}'.format('Price:'))
        statusFile.write('{0:>6.1f}'.format((m.bid+m.ask)/2) + '\n')
        statusFile.write('{0:<10}'.format('EUR:'))
        statusFile.write('{0:>6.1f}'.format(p.EUR) + '\n')
        statusFile.write('{0:<10}'.format('BTC:'))
        statusFile.write('{0:>6.1f}'.format(p.BTC) + '\n')

def printTermLine(p, m, t):
    strLog = '{0:<10}'.format(m.time) + ' |'
    strLog += ' B:'+ '{0:>7.1f}'.format(m.bid) 
    strLog += ' A:'+ '{0:>7.1f}'.format(m.ask) + ' |'
    strLog += ' EUR:' + '{0:>6.1f}'.format(p.EUR)
    strLog += ' BTC:' + '{0:>7.3f}'.format(p.BTC) + ' |'
    strLog += ' Bounds:' + '{0:>6.1f}'.format(t.minPrice) 
    strLog += '{0:>7.1f}'.format(t.maxPrice) + ' |'
    strLog += ' Trade: ' + '{0:>6.1f}'.format(t.coinsToTrade) 
    print(strLog)
    sys.stdout.flush()
    return 0
