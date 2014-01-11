from bbClasses import *
from bbFunctions import *
import time
import sys
import re
import os.path

start_time = time.time()

with open(logFileNameBT, 'w') as logBT:
    logBT.write('Time,Bid,Ask,EUR,BTC,Trade\n')

t = trader(logFileNameBT)
p = portfolio(1500, 0)
m = marketData('2013-12-25 22:11:00', 493.3, 495.7)
printLogLine(p, m, t, logFileNameBT)

for i in range(1,file_len(logFileName)):
#for i in range(1,100):
    
    t.calcBaseWeight(m)
#    print(t.calcMomentum(m))
    
    t.calcCoinsToTrade(m, p)

    t.checkTradeSize()

    strLog = m.time
    strLog = strLog + ' | B: '+str(round(m.bid,1))+' A: '+str(round(m.ask,1))
    strLog = strLog + ' | EUR: ' + str(round(p.EUR,1)) + ' | BTC: ' + str(round(p.BTC,3))
    strLog = strLog + ' | Bounds: ' + str(round(t.minPrice,1)) + ' ' + str(round(t.maxPrice,1))
    strLog = strLog + ' | Trade: ' + str(round(t.coinsToTrade,3)) + '\n'
    if abs(t.coinsToTrade) >= 0.5:
        sys.stdout.write(strLog)
        sys.stdout.flush()
    printLogLine(p, m, t, logFileNameBT)

    p.BTC = p.BTC + t.coinsToTrade
    if t.coinsToTrade > 0:
        p.EUR = p.EUR - t.coinsToTrade * m.ask
    elif t.coinsToTrade < 0:
        p.EUR = p.EUR - t.coinsToTrade * m.bid

    m, p = testData(logFileName, m, p, i)
    t = trader(logFileNameBT)

print time.time() - start_time, "seconds"    
