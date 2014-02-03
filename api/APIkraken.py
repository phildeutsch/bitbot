import json
import urllib
import urllib2
 
import hashlib
import hmac
import base64
 
import time
 
 
class APIkraken(object):
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
        postdata = urllib.urlencode(req)
         
        headers = {
            'User-Agent': 'Kraken Python API Agent'
        }
         
        url = self.uri + '/' + self.apiversion + '/public/' + method
        ret = urllib2.urlopen(urllib2.Request(url, postdata, headers))
        return json.loads(ret.read())
     
    def query_private(self, method, req={}):
        """API queries that require a valid key/secret pair.
         
        Arguments:
        method -- API method name (string, no default)
        req    -- additional request parameters (default {})
         
        """
        req['nonce'] = int(1000*time.time())
        postdata = urllib.urlencode(req)
         
        urlpath = '/' + self.apiversion + '/private/' + method
        message = urlpath + hashlib.sha256(str(req['nonce']) +
                                            postdata).digest()
        signature = hmac.new(base64.b64decode(self.secret),
                             message, hashlib.sha512)
         
        headers = {
            'User-Agent': 'Kraken Python API Agent',
            'API-Key': self.key,
            'API-Sign': base64.b64encode(signature.digest())
        }
         
        url = self.uri + urlpath
        ret = urllib2.urlopen(urllib2.Request(url, postdata, headers))
        return json.loads(ret.read())
