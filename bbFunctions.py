from bbClasses import *
from bbSettings import *
import linecache
import time
import sys
import re
import os.path

def printLogLine(p, m, t, logFileName):
    with open(logFileName,'a') as logFile:
        logFile.write(m.time + ',')
        logFile.write(str(m.bid) + ',')
        logFile.write(str(m.ask) + ',')
        logFile.write(str(p.EUR) + ',')
        logFile.write(str(p.BTC) + ',')
        logFile.write(str(t.coinsToTrade) + '\n')

def placeOrder(krakenAPI, trader):
    if abs(trader.coinsToTrade) > minTrade:
        if coinsToTrade < 0:
            trade = krakenAPI.query_private('AddOrder', {
                'pair' : 'XXBTZEUR',
                'type' : 'sell', 
                'ordertype' : 'limit',
                'price' : tradePrice, 
                'volume' : -coinsToTrade
            })
            trader.error = 0
        else:
            trade = api.query_private('AddOrder', {
                'pair' : 'XXBTZEUR',
                'type' : 'buy',
                'ordertype' : 'limit',
                'price' : tradePrice,
                'volume' : coinsToTrade
             })
            trader.error = 0
        if trade['error'] != []:
            trader.error = 1

def cancelOrders(krakenAPI):
    openOrders = krakenAPI.query_private('OpenOrders')['result']
    if openOrders['open'] != {}:
        for transaction in openOrders['open'].keys():
            krakenAPI.query_private('CancelOrder', {'txid':transaction})

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

def getHistoricMax(logFileName):
    with open(logFileName,'r') as logFile:
        history = logFile.readlines()
    maxPrice = float(re.split(',', history[1])[2])
    for line in range(2,len(history)):
        if float(re.split(',', history[line])[2]) > maxPrice:
            maxPrice = float(re.split(',', history[line])[2])
    return maxPrice

def testData(logFile, m, p, i):
    data = re.split(',', linecache.getline(logFile, i+1))
    m.time = data[0]
    m.bid = float(data[1])
    m.ask = float(data[2])

    p.weight = p.EUR / (p.EUR + p.BTC * m.bid)

    return m, p

def file_len(fname):
    with open(fname) as f:
        for i, l in enumerate(f):
            pass
    return i + 1

