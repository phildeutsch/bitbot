import sys
sys.path.append('./source')

from bbKeys import *
from bbClasses import *
from bbSettings import *
from bbFunctions import *
import krakenex

t         = trader(logFileName, walkUp, walkDown, midDistance, tradeBuffer,
                    priceWindow)
p         = portfolio(1,0)
m         = marketData('Null', 0, 0, priceWindow)
krakenAPI = krakenex.API(key, secret)
m, p = getData(krakenAPI, m, p, t)

print('Current Value: ' + '{0:4.0f}'.format(p.value))
action = raw_input('What do you want to do? (f)und, (w)ithdraw: ')
if action is 'f':
    amt = raw_input('Amount (BTC) to fund: ')
    with open(transferFile, 'at') as txFile:
        txFile.write(m.time + ',')
        txFile.write(str(m.bid) + ',')
        txFile.write(str(m.ask) + ',')
        txFile.write(str(amt) + '\n')
else:
    print('I do not know what you want to do.')
