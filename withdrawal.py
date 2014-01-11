from btcTraderSettings import *
from btcTraderFunctions import *
import krakenex

api = krakenex.API(key, secret)
maxValue = 1500
minTransfer = 0.02
transferFileName = 'btcTraderTransfers.csv'

tickTime = api.query_public('Time')['result']['rfc1123']
tickData = api.query_public('Ticker', {'pair' : 'XXBTZEUR'})
balance  = api.query_private('Balance')['result']
bidPrice = float(tickData['result']['XXBTZEUR']['b'][0])
askPrice = float(tickData['result']['XXBTZEUR']['a'][0])
holdEUR  = float(balance['ZEUR'])
holdBTC  = float(balance['XXBT'])

totValue      = holdEUR + holdBTC * bidPrice
btcToTransfer = (totValue - maxValue) / askPrice
if btcToTransfer > minTransfer and btcToTransfer < holdBTC:
    print 'Transfer ' + str(btcToTransfer) + ' BTC.'
    logChoice = raw_input('Log transfer (y/n)?: ')
    if logChoice == 'y':
        with open(transferFileName, 'a') as transferFile:
            transferFile.write(','.join([
                tickTime[5:20], 
                str(bidPrice),
                str(askPrice),
                str(btcToTransfer),
                '\n']))    
elif btcToTransfer > 0:
    print 'Not enough btc for transfer'
else:
    print 'Leave the money alone!'
