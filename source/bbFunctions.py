from smtplib import SMTP_SSL as SMTP
from email.mime.text import MIMEText
from collections import deque
import linecache
import time
import sys
import re

def getHistPrices(logFileName, priceWindow):
    histPrices = deque([], priceWindow)
    with open(logFileName, 'rt') as f:
        data = f.readlines()
    for i in range(priceWindow):
        bid=float(data[-priceWindow+i].split(',')[1])
        ask=float(data[-priceWindow+i].split(',')[2])
        histPrices.append((bid+ask)/2)
    return histPrices

def sendEmail(t, recipient, subject):
    text = ''
    msg = MIMEText(text, 'plain')
    smtpServer = 'smtpout.europe.secureserver.net'
    login = 'phil@phildeutsch.com'
    pwd = 'Dezember2013'
    msg['To'] = recipient
    msg['From'] = login
    msg['Subject'] = subject
    try:
        conn = SMTP(smtpServer)
        conn.login(login, pwd)
        conn.sendmail(login, recipient, msg.as_string())
        conn.close()
    except:
        t.error = 'Error sending email.'

def drawPlot(m, t, plotFile):
    plotFileHead   = 'source/plotHead.txt'
    plotFileTail   = 'source/plotTail.txt'

    if t.coinsToTrade is 0:
        t.buys.append('null')
        t.sells.append('null')
    elif t.coinsToTrade > 0:
        t.buys.append(m.ask)
        t.sells.append('null')
    elif t.coinsToTrade < 0:
        t.buys.append('null')
        t.sells.append(m.bid)

    with open(plotFile,'w') as picFile:
        with open(plotFileHead,'rt') as file1:
            content = file1.readlines()
            picFile.write(''.join(content))

        for i in range(min(len(m.histPrices), len(t.buys))):
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

def printLogLine(m, p, t, logFileName, bounds=0):
    with open(logFileName,'a') as logFile:
        logFile.write(m.time + ',')
        logFile.write('{0:0.2f}'.format(m.bid) + ',')
        logFile.write('{0:0.2f}'.format(m.ask) + ',')
        logFile.write('{0:0.2f}'.format(p.EUR) + ',')
        logFile.write('{0:0.6f}'.format(p.BTC) + ',')
        logFile.write('{0:0.2f}'.format(t.coinsToTrade))
        if bounds is 1:
            logFile.write(',' + '{0:0.2f}'.format(t.minPrice))
            logFile.write(',' + '{0:0.2f}'.format(t.maxPrice))
        logFile.write('\n')

def printStatus(m, p, t, statusFileName, freezeFileName):
    with open(statusFileName, 'w') as statusFile:
        statusFile.write('{0:<10}'.format('Time:'))
        statusFile.write('{0:<10}'.format(m.time) + '\n')
        statusFile.write('{0:<10}'.format('Status:'))
        if t.suspend is 0:
            if t.override is 1:
                statusFile.write('{0:<10}'.format('Trading to external target') + '\n')
            elif t.override is 0:
                statusFile.write('{0:<10}'.format('Autonomous trading') + '\n')
        elif t.suspend is 1:
            statusFile.write('{0:<10}'.format('Trading suspended') + '\n')
        statusFile.write('{0:<10}'.format('Price:'))
        statusFile.write('{0:>6.1f}'.format((m.bid+m.ask)/2) + '\n')
        statusFile.write('{0:<10}'.format('EUR:'))
        statusFile.write('{0:>6.1f}'.format(p.EUR) + '\n')
        statusFile.write('{0:<10}'.format('BTC:'))
        statusFile.write('{0:>7.2f}'.format(p.BTC) + '\n')
        statusFile.write('{0:<10}'.format('Value:'))
        statusFile.write('{0:>6.1f}'.format(p.EUR + p.BTC * m.bid) + '\n')
        statusFile.write('\n')
        statusFile.write('{0:<10}'.format('minPrice:'))
        statusFile.write('{0:>7.2f}'.format(t.minPrice) + '\n')
        statusFile.write('{0:<10}'.format('maxPrice:'))
        statusFile.write('{0:>7.2f}'.format(t.maxPrice) + '\n')
        statusFile.write('{0:<10}'.format('Allin:'))
        statusFile.write('{0:>7.2f}'.format(m.high * (1 - t.allinLimit)) + '\n')
        statusFile.write('{0:<10}'.format('Stoploss:'))
        statusFile.write('{0:>7.2f}'.format(m.high * (1 - t.stopLossLimit)) + '\n')

def printTermLine(m, p, t):
    strLog = '{0:<10}'.format(m.time[0:16]) + ' |'
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
