from bbSettings import *

import random
import numpy  as np
import pandas as pd

history = pd.read_csv(logFileName, parse_dates=[0], index_col=0)
history['Price'] = (history['Bid']+history['Ask'])/2
history['Return']= history.pct_change()['Price']
mu  = history.mean()['Return']
sig = history.std()['Return']

random.seed()
hist = np.genfromtxt('data/hist.csv', delimiter=',', skip_header = True)

for runs in range(10):
    r = random.random()
    for i in range(len(hist)):
        if r <hist[i][2]:
            ret = hist[i][0]
            break
    print(ret)
