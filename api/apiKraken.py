import json
import urllib.parse
import urllib.request
 
import hashlib
import hmac
import base64
 
import time
import datetime
 
 
class API(object):
    """Kraken.com cryptocurrency Exchange API.
     
    Public methods:
    query_public
    query_private
     
    """
     
    def __init__(self, key = '', secret = ''):
        """Create an object with authentication information.
         
        Arguments:
        key    -- key required to make queries to the API (default '')
        secret -- private key used to sign API messages (default '')
         
        """
        self.key = key
        self.secret = secret
        self.uri = 'https://api.kraken.com'
        self.apiversion = '0'
     
    def query_public(self, method, req = {}):
        """API queries that do not require a valid key/secret pair.
         
        Arguments:
        method -- API method name (string, no default)
        req    -- additional request parameters (default {})
         
        """
        postdata = urllib.parse.urlencode(req)
        postdata = postdata.encode('latin1')
         
        headers = {
            'User-Agent': 'phildeutsch.com'
        }
         
        url = self.uri + '/' + self.apiversion + '/public/' + method
        ret = urllib.request.urlopen(urllib.request.Request(url, postdata, headers))
        return json.loads(ret.read().decode('latin1'))
     
    def query_private(self, method, req={}):
        """API queries that require a valid key/secret pair.
         
        Arguments:
        method -- API method name (string, no default)
        req    -- additional request parameters (default {})
         
        """
        req['nonce'] = int(1000*time.time())
        postdata = urllib.parse.urlencode(req)
         
        urlpath = '/' + self.apiversion + '/private/' + method
        message = hashlib.sha256(
           (str(req['nonce']) + postdata).encode('latin1')).digest()
        message = urlpath + message.decode('latin1')
        message = message.encode('latin')
        signature = hmac.new(base64.b64decode(self.secret.encode('latin1')),
                             message, hashlib.sha512)
        
        headers = {
            'User-Agent': 'phildeutsch.com',
            'API-Key': self.key,
            'API-Sign': base64.b64encode(signature.digest())
        }
        postdata = postdata.encode('latin1')
         
        url = self.uri + urlpath
        ret = urllib.request.urlopen(urllib.request.Request(url, postdata, headers))
        return json.loads(ret.read().decode('latin1'))
		
    def getDepth(self, count):
        depth = self.query_public('Depth', {
                                 'pair' : 'XXBTZEUR',
                                 'count': count})
        asks = depth['result']['XXBTZEUR']['asks']
        bids = depth['result']['XXBTZEUR']['bids']
        return bids, asks
		
    def getPrices(self, m, coinsToTrade):
        b, a = self.getDepth(10)
        bid = 0
        ask = 0
        coinsToTrade   = abs(coinsToTrade)
          
        if coinsToTrade < float(a[0][1]):
            ask = float(a[0][0])
        else:
            cumDepth = 0
            for i in range(len(a)):
                cumDepth += float(a[i][1])
                if cumDepth > coinsToTrade:
                    ask = a[i][0]
                    break
        if ask == 0:
            ask = a[-1][0]
                    
        if coinsToTrade < float(b[0][1]):
            bid = float(b[0][0])
        else:
            cumDepth = 0
            for i in range(len(b)):
                cumDepth += float(b[i][1])
                if cumDepth > coinsToTrade:
                    bid = b[i][0]
                    break
        if bid == 0:
            bid = b[-1][0]

        m.bid = float(bid)
        m.ask = float(ask)
        m.price = (m.bid + m.ask)/2
        m.histPrices.append(m.price)
        m.mean = sum(m.histPrices)/len(m.histPrices)
        m.time = datetime.datetime.now().isoformat()
            
        return m.bid, m.ask
        
    def getBalance(self, m, p, t):
        balance  = self.query_private('Balance')['result']
        p.EUR  = float(balance['ZEUR'])
        p.BTC  = float(balance['XXBT'])
        p.value = p.EUR + p.BTC * m.bid
        p.weight = p.EUR / p.value
        t.minTrade = t.tradeFactor * p.value
        return p.value
