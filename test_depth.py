import sys
sys.path.append('./source')
sys.path.append('./api')
import apiKraken
from bbClasses import *
from bbSettings import *
from bbFunctions import *
from bbKeysMonitor import *

krakenAPI = apiKraken.API(keyKraken, secKraken)
count = 5
b, a = apiKraken.getDepth(krakenAPI, count)
coinsToTrade = -2.2
tradePrice = 0
if coinsToTrade > 0:
    if coinsToTrade < float(a[0][1]):
        tradePrice = float(a[0][0])
    else:
        cumDepth = 0
        for i in range(len(a)):
            cumDepth += float(a[i][1])
            if cumDepth > coinsToTrade:
                tradePrice = a[i][0]
                break
    if tradePrice is 0:
            tradePrice = a[count][0]
elif coinsToTrade < 0:
    if coinsToTrade > float(b[0][1]):
        tradePrice = float(b[0][0])
    else:
        cumDepth = 0
        for i in range(len(b)):
            cumDepth += float(b[i][1])
            if cumDepth > -coinsToTrade:
                tradePrice = b[i][0]
                break
    if tradePrice is 0:
            tradePrice = b[count][0]

print(coinsToTrade, tradePrice)   
