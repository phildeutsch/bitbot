bitbot - algortihmic trader for kraken

Dependencies:

krakenex (https://github.com/veox/krakenex)

Settings:

Missing from this repository is a file "bbSettings.py" which should contain the
following lines:

key          = kraken api key string
secret       = kraken api secret string
delay        = delay between api calls
maxWalk      = maximum relative difference between peak and minimum
midDistance  = relative point between minimum and peak price
tradeBuffer  = percentage of funds reserved for momentum trading
logFileName  = 'Logs/history.csv'
logFileNameBT= 'Logs/historyBT.csv'

