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
for walkUp in [0.15]:
    for walkDown in [0]:
        for minTrade in [0.75]:
            logFileNameBT = 'Logs/' + str(walkUp) + str(walkDown) + str(minTrade) + '.bt'
            with open(logFileNameBT, 'w') as logBT:
                logBT.write('Time,Bid,Ask,EUR,BTC,Trade\n')

            t = trader(logFileNameBT, walkUp, walkDown, midDistance, tradeBuffer)
            p = portfolio(funds, 0)
            m = marketData('2013-12-25 22:11:00', 493.3, 495.7)
            printLogLine(p, m, t, logFileNameBT)

            #for i in range(1,file_len(logFileName)):
            for i in range(1,100):
                
                t.calcBaseWeight(m)
            #    print(t.calcMomentum(m))
                
                t.calcCoinsToTrade(m, p)

                t.checkTradeSize(minTrade)

                if abs(t.coinsToTrade) >= minTrade:
                    printTermLine(p, m, t)
                printLogLine(p, m, t, logFileNameBT)

                p.BTC = p.BTC + t.coinsToTrade
                if t.coinsToTrade > 0:
                    p.EUR = p.EUR - t.coinsToTrade * m.ask
                elif t.coinsToTrade < 0:
                    p.EUR = p.EUR - t.coinsToTrade * m.bid

                m, p = getDataBacktest(logFileName, m, p, i)
                t = trader(logFileNameBT, walkUp, walkDown, midDistance, tradeBuffer)
          
            data = pd.read_csv(logFileNameBT)
            data['Value'] = data['EUR'] + data['BTC'] * data['Bid']
            r = np.mean(data['Value'].pct_change())
            s = np.std(data['Value'].pct_change())
            sharpe = r/s * 100
            
            data = re.split(',', linecache.getline(logFileNameBT, file_len(logFileNameBT)))
#            os.remove(logFileNameBT)
            endValue = float(data[3]) + float(data[4]) * float(data[1])
            endRet   = (endValue/funds - 1) * 100
            print('Return: ' + str(endRet) + '%')
            results.append([walkUp, walkDown, minTrade, endRet, sharpe])
            

results = np.array(results)
print(results[results[:,4].argsort()][::-1])

#print time.time() - start_time, "seconds"    
