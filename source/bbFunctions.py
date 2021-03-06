from smtplib import SMTP_SSL as SMTP
from email.mime.text import MIMEText
import bbCfg
import linecache
import time
import sys
import re
import math
import hashlib
from collections import OrderedDict
from imp import reload

def display_config():
    varList = [var for var in dir(bbCfg) if not var.startswith("_")]
    numList = [var for var in varList if is_number(eval('bbCfg.'+var))]
    numList = sorted(numList)
    for var in sorted(numList):
        sys.stdout.write('{0:<20}'.format(var))
        sys.stdout.write(str(eval('bbCfg.'+var)) + '\n')
    print('')
    return 0

def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        return False

def getLogFileNameBT():
    varList = [var for var in dir(bbCfg) if not var.startswith("_")]
    numList = [var for var in varList if is_number(eval('bbCfg.'+var))]
    numList = sorted(numList)
    varDict = OrderedDict()
    for var in numList:
        varDict[var] = eval('bbCfg.'+ var)
#   print(varDict)
    h = hashlib.md5(str(varDict).encode('utf-8')).hexdigest()
    return 'data/logBT' + h + '.csv'

def progressBarLength():
    return math.floor(file_len(bbCfg.logFileName)/bbCfg.progressBar)

def choose_parameters():
    sys.stdout.write('Choose Parameter to change:\n')
    sys.stdout.write(' x) Done\n')
    sys.stdout.write(' d) Display current values\n')
    sys.stdout.write(' s) Restore standard values\n')
    varList = [var for var in dir(bbCfg) if not var.startswith("_")]
    numList = [var for var in varList if is_number(eval('bbCfg.'+var))]
    numList = sorted(numList)
    for i in range(len(numList)):
        sys.stdout.write('{0:>2}'.format(i) + ') ')
        sys.stdout.write(numList[i])
        sys.stdout.write('\n')

    paramChoice = input('')
    if paramChoice == 'd':
        display_config()
        choose_parameters()
    elif paramChoice == 's':
        reload(bbCfg)
        choose_parameters()
    elif paramChoice == 'x':
        pass
    elif is_number(paramChoice):
        newValue = input('Enter new value for ' +
                        str(numList[int(paramChoice)]) + ':\n')
        exec('bbCfg.' + numList[int(paramChoice)] + ' = ' + newValue)
        choose_parameters()

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

def drawPlot(m, t):
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

    with open(bbCfg.plotFileName,'w') as picFile:
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

def getBounds(logFileName):
    with open(logFileName,'r') as logFile:
        history = logFile.readlines()
    maxPrice = float(re.split(',', history[1])[2])
    minPrice = float(re.split(',', history[1])[1])
    for line in range(2,len(history)):
        if float(re.split(',', history[line])[2]) > maxPrice:
            maxPrice = float(re.split(',', history[line])[2])
            minPrice = maxPrice * (1 - bbCfg.walkDown)
        if float(re.split(',', history[line])[1]) < minPrice:
            minPrice = float(re.split(',', history[line])[1])
            maxPrice = minPrice * (1 + bbCfg.walkUp)
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

def printStatus(m, p, t):
    with open(bbCfg.statusFileName, 'w') as statusFile:
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
        statusFile.write('{0:>7.2f}'.format(m.high * (1 - bbCfg.allinLimit)) + '\n')
        statusFile.write('{0:<10}'.format('Stoploss:'))
        statusFile.write('{0:>7.2f}'.format(m.high * (1 - bbCfg.stopLossLimit)) + '\n')

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
