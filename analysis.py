import sys
sys.path.append('./source')
from bbSettings import *

import random
import numpy  as np
import pandas as pd

history = pd.read_csv(logFileName, parse_dates=[0], index_col=0)
history['Price'] = (history['Bid']+history['Ask'])/2
history['Return']= history.pct_change()['Price']
history['Return'][0] = 0
mu  = history.mean()['Return']
sig = history.std()['Return']

c, d = np.histogram(history['Return'], bins = 100)
histo = pd.DataFrame({'Delimiter' : d[1:], 'Count' : c})
obs = histo.sum()['Count']
histo['Probability'] = histo['Count']/obs+
histo['CumProb'] = histo.cumsum()['Probability']
