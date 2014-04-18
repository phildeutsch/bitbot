import sys

sys.path.append('./source')
sys.path.append('./api')

import bbCfg
import bbFunctions
import bbClasses
import bitbot
import apiKraken

from bbKeys import *

t = bbClasses.trader(bbCfg.logFileName)
p = bbClasses.portfolio(100,0)
m = bbClasses.marketData('Null', 500, 500)
API = apiKraken.API(keyKraken, secKraken)

bitbot.mainLoop(m, p, t, API, 0, 0)

