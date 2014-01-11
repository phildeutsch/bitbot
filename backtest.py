from bbSettings import *
from bbClasses import *
from bbFunctions import *
import time
import sys
import re
import os.path
import linecache
import numpy as np
import pandas as pd

#start_time = time.time()

results = []
for walkUp in [0.1, 0.15, 0.2]:
    for walkDown in [0.03, 0.05]:
        for minTrade in [1.0, 1.25, 1.5]:
            logFileNameBT = 'Logs/' + str(walkUp) + str(walkDown) + str(minTrade) + '.bt'
            with open(logFileNameBT, 'w') as logBT:
                logBT.write('Time,Bid,Ask,EUR,BTC,Trade\n')

            t = trader(logFileNameBT, walkUp, walkDown, midDistance, tradeBuffer)
            p = portfolio(funds, 0)
            m = marketData('2013-12-25 22:11:00', 493.3, 495.7)
            printLogLine(p, m, t, logFileNameBT)

            for i in range(1,file_len(logFileName)):
            #for i in range(1,100):
                
                t.calcBaseWeight(m)
            #    print(t.calcMomentum(m))
                
                t.calcCoinsToTrade(m, p)

                t.checkTradeSize(minTrade)

                strLog = m.time
                strLog = strLog + ' | B: '+str(round(m.bid,1))+' A: '+str(round(m.ask,1))
                strLog = strLog + ' | EUR: ' + str(round(p.EUR,1)) + ' | BTC: ' + str(round(p.BTC,3))
                strLog = strLog + ' | Bounds: ' + str(round(t.minPrice,1)) + ' ' + str(round(t.maxPrice,1))
                strLog = strLog + ' | Trade: ' + str(round(t.coinsToTrade,3)) + '\n'
    #            if abs(t.coinsToTrade) >= minTrade:
    #                sys.stdout.write(strLog)
    #                sys.stdout.flush()
                printLogLine(p, m, t, logFileNameBT)

                p.BTC = p.BTC + t.coinsToTrade
                if t.coinsToTrade > 0:
                    p.EUR = p.EUR - t.coinsToTrade * m.ask
                elif t.coinsToTrade < 0:
                    p.EUR = p.EUR - t.coinsToTrade * m.bid

                m, p = testData(logFileName, m, p, i)
                t = trader(logFileNameBT, walkUp, walkDown, midDistance, tradeBuffer)
          
            data = pd.read_csv(logFileNameBT)
            data['Value'] = data['EUR'] + data['BTC'] * data['Bid']
            m = np.mean(data['Value'].pct_change())
            s = np.std(data['Value'].pct_change())
            sharpe = m/s * 100
            
            data = re.split(',', linecache.getline(logFileNameBT, file_len(logFileName)+1))
            os.remove(logFileNameBT)
            endValue = float(data[3]) + float(data[4]) * float(data[1])
            endRet   = (endValue/funds - 1) * 100
            print 'Return: ' + str(endRet) + '%'
            results.append([walkUp, walkDown, minTrade, endRet, sharpe])
            

results = np.array(results)
print results[results[:,4].argsort()][::-1]

#print time.time() - start_time, "seconds"    
