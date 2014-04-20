import sys

sys.path.append('./source')
sys.path.append('./api')

import bbCfg
import bbFunctions
import bbClasses
import bitbot
import apiKraken
import apiBacktest

from bbKeys import *

t = bbClasses.trader(bbCfg.logFileName)
p = bbClasses.portfolio(100,0)
m = bbClasses.marketData('Null', 500, 500)
apiK = apiKraken.API(keyKraken, secKraken)
apiB = apiBacktest.API()

print('\nTesting normal trading')
bitbot.mainLoop(m, p, t, apiK, 0, 0)

print('\nTesting test mode')
bitbot.mainLoop(m, p, t, apiK, 1, 0)

print('\nTesting backtesting')
bitbot.main('-b')

print('\nTesting backtest + test mode')
bitbot.mainLoop(m, p, t, apiB, 1, 1)

print('\nTesting trader error')
t.error='Test error'
bitbot.mainLoop(m, p, t, apiK, 0, 0)

print('\nTesting stop loss')
m.high = 99999
t.stopLoss(m,p)
with open(bbCfg.overrideFileName, 'wt') as of:
    of.write('override = ' + str(0) + '\n')
    of.write('target   = ' + str(0) + '\n')
    of.write('suspend  = ' + str(0) + '\n')

