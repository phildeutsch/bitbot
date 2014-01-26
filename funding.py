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
