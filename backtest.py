from bbSettings import *
from bbClasses import *
from bbFunctions import *

from re import split
from linecache import getline
from collections import deque

import numpy as np
import pandas as pd

results = []
for tradeBuffer in [0]:
    for priceWindow in [100]:
        for momFactor in [0.75]:
            for midDistance in [0.5]:
                for walkUp in [0.15]:
                    for walkDown in [0]:
                        for minTrade in [0.75]:
                            logFileNameBT  = 'Logs/' + str(tradeBuffer)
                            logFileNameBT += str(priceWindow)
                            logFileNameBT += str(momFactor)
                            logFileNameBT += str(midDistance)
                            logFileNameBT += str(walkUp)
                            logFileNameBT += str(walkDown)
                            logFileNameBT += str(minTrade) + '.bt'
                            
                            with open(logFileNameBT, 'w') as logBT:
                                logBT.write('Time,Bid,Ask,EUR,BTC,Trade\n')

                            t = trader(logFileNameBT, walkUp, walkDown, midDistance, tradeBuffer)
                            p = portfolio(funds, 0)
                            m = marketData('2013-12-25 22:11:00', 493.3, 495.7, priceWindow)
                            printLogLine(p, m, t, logFileNameBT)

                            #for i in range(1,file_len(logFileName)):
                            for i in range(1,1000):
                                
                                t.calcBaseWeight(m)
                                t.calcMomentum(momFactor, m)
                                t.calcCoinsToTrade(m, p)
                                t.checkTradeSize(minTrade)

                                #if abs(t.coinsToTrade) >= minTrade:
                                #    printTermLine(p, m, t)

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
                            
                            data = re.split(',',
                                        linecache.getline(logFileNameBT, file_len(logFileNameBT)))

                            endValue = float(data[3]) + float(data[4]) * float(data[1])
                            endRet   = (endValue/funds - 1) * 100
                            #print('Return: ' + str(endRet) + '%')
                            results.append([tradeBuffer,
                                            priceWindow,
                                            momFactor,
                                            midDistance,
                                            walkUp,
                                            walkDown,
                                            minTrade,
                                            round(endRet,2),
                                            round(sharpe,2)])
                            #os.remove(logFileNameBT)      

results = np.array(results)
print('tradeBuffer, priceWindow, momFactor, midDistance, walkUp, walkDown, minTrade, Return, Sharpe')
print(results[results[:,8].argsort()][::-1])

