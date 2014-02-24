import sys

sys.path.append('./source')
sys.path.append('./api')

import apiBitstamp
from bbKeys import *


public_client = apiBitstamp.Public()
print(public_client.ticker()['volume'])
