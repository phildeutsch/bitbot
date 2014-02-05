import sys
sys.path.append('./source')
from bbSettings import *
from bbClasses import *
from bbFunctions import *

from re import split
from linecache import getline
from collections import deque

import numpy as np
import pandas as pd
np.set_printoptions(precision=4, suppress=True)
funds = 2000
results = []
for tradeBuffer in [0]:
    for priceWindow in [100]:
        for momFactor in [0.75]:
            for midDistance in [0.5]:
                for walkUp in [0.15]:
                    for walkDown in [0]:
                        logFileNameBT  = 'data/' + str(tradeBuffer)
                        logFileNameBT += str(priceWindow)
                        logFileNameBT += str(momFactor)
                        logFileNameBT += str(midDistance)
                        logFileNameBT += str(walkUp)
                        logFileNameBT += str(walkDown) + '.csv'
                        
                        with open(logFileNameBT, 'w') as logBT:
                            logBT.write('Time,Bid,Ask,EUR,BTC,Trade,minTrade,maxTrade\n')

                        t = trader(logFileNameBT, walkUp, walkDown,
                                midDistance, tradeBuffer, priceWindow)
                        p = portfolio(funds, 0)
                        m = marketData('Null', 0, 0, priceWindow)

                        for i in range(1,file_len(logFileName)):
#                        for i in range(1,100):
                           
                            t = trader(logFileNameBT, walkUp, walkDown,
                                    midDistance, tradeBuffer, priceWindow)
                            m, p = getDataBacktest(logFileName,  m, p, t, i)
                            
                            t.calcBaseWeight(m)
                            t.calcMomentum(momFactor, m)
                            t.calcCoinsToTrade(m, p)
                            t.checkTradeSize(m, p, tradeFactor)
            
#                           if abs(t.coinsToTrade) > 0:
#                               printTermLine(m, p, t)

                            printLogLine(m, p, t, logFileNameBT, bounds = 1)

                            p.BTC = p.BTC + t.coinsToTrade
                            if t.coinsToTrade > 0:
                                p.EUR = p.EUR - t.coinsToTrade * m.ask
                            elif t.coinsToTrade < 0:
                                p.EUR = p.EUR - t.coinsToTrade * m.bid

                        data = pd.read_csv(logFileNameBT)
                        data['Value'] = (data['EUR'] +
                                         data['BTC'] * data['Bid'])
                        r = np.mean(data['Value'].pct_change())
                        s = np.std(data['Value'].pct_change())
                        sharpe = r/s * 100
                        
                        lastline = re.split(',',
                                linecache.getline(logFileNameBT,
                                file_len(logFileNameBT)))

                        endValue = (float(lastline[3]) +
                                    float(lastline[4]) * float(lastline[1]))
                        endRet   = (endValue/funds - 1) * 100
                        print('Return: ' + str(endRet) + '%')
                        results.append([tradeBuffer,
                                        priceWindow,
                                        momFactor,
                                        midDistance,
                                        walkUp,
                                        walkDown,
                                        round(endRet,2),
                                        round(sharpe,2)])
                        #os.remove(logFileNameBT)      

results = np.array(results)
print('tradeBuffer, priceWindow, momFactor, midDistance, walkUp, walkDown,' + 
      'Return, Sharpe')
print(results[results[:,7].argsort()][::-1])
drawPlot(plotFileHead, plotFileTail, m, t)

