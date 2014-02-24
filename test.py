import sys

sys.path.append('./source')
sys.path.append('./api')

import apiBitstamp
from bbKeys import *


public_client = apiBitstamp.Public()
print(public_client.ticker()['volume'])
trading_client = apiBitstamp.Trading(
    username = '370147',
    key = keyBitstamp,
    secret = secBitstamp)
print(trading_client.account_balance())
