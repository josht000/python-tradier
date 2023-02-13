import json

class Order():
    def __init__(self) -> None:
        self._class = None # equity
        self.symbol:str = None
        self.side:str = None # buy, buy_to_cover, sell, sell_short
        self.quantity: int = None
        self.type: str = None # market, limit, stop, stop_limit
        self.price: str = None # optional for market orders
        self.stop: str = None  # optional unless a stop type order

class Tradier():
    def __init__(self, httpclient, token):
        self.httpclient = httpclient
        self.token = token
        self.user = Tradier.User(self)
        self.accounts = Tradier.Accounts(self)
        self.markets = Tradier.Markets(self)
        self.fundamentals = Tradier.Fundamentals(self)
        self.options = Tradier.Options(self)
        self.watchlists = Tradier.Watchlists(self)
        self.order = Tradier.Order(self)
        self.account_id = None

    def request(
            self,
            method,
            path,
            headers=None,
            params=None,
            data=None,
            callback=None):

        # print('token=', self.token)
        headers = headers or {}
        headers['Authorization'] = 'Bearer %s' % self.token
        headers['Accept'] = 'application/json'

        def base_callback(response):
            if response.code != 200:
                raise Exception(response.code, response.body)
            return json.loads(response.body)

        if callback == None:
            cb = base_callback
        else:
            cb = lambda x: callback(base_callback(x))

        r = self.httpclient.request(
                cb,
                method,
                path,
                headers=headers,
                params=params,
                data=data)
        return r

    class User():
        def __init__(self, agent):
            self.agent = agent

        def profile(self):
            response = self.agent.request('GET', 'user/profile')
            return response

        def balances(self):
            response = self.agent.request('GET', 'user/balances')
            return response

    class Accounts():
        '''Gets account status like current orders. '''

        def __init__(self, agent):
            self.agent = agent

        def orders(self, account_id):
            response = self.agent.request(
                'GET', 'accounts/%s/orders' % account_id)
            return response['orders']['order']

        def order(self, account_id, order_id):
            response = self.agent.request(
                'GET', 'accounts/%s/orders/%s' % (account_id, order_id))
            return response

    class Markets():
        def __init__(self, agent):
            self.agent = agent

        def quotes(self, symbols):
            def callback(response):
                quote = response['quotes'].get('quote', [])
                if not isinstance(quote, list):
                    quote = [quote]
                return quote
            return self.agent.request(
                'GET',
                'markets/quotes',
                params={'symbols': ','.join(symbols)},
                callback=callback)

    class Fundamentals():
        def __init__(self, agent):
            self.agent = agent

        def calendars(self, symbols):
            def callback(response):
                return response
            return self.agent.request(
                'GET',
                'markets/fundamentals/calendars',
                params={'symbols': ','.join(x.upper() for x in symbols)},
                callback=callback)

    class Options():
        def __init__(self, agent):
            self.agent = agent

        def expirations(self, symbol):
            return self.agent.request(
                'GET',
                'markets/options/expirations',
                params={'symbol': symbol},
                callback=(lambda x: x['expirations']['date']))

        def chains(self, symbol, expiration):
            def callback(response):
                if response['options']:
                    return response['options']['option']
                return []
            return self.agent.request(
                'GET',
                'markets/options/chains',
                params={'symbol': symbol, 'expiration': expiration},
                callback=callback)

    class Watchlists():
        def __init__(self, agent):
            self.agent = agent

        def __call__(self):
            response = self.agent.request('GET', 'watchlists')
            return response['watchlists']['watchlist']

        def get(self, watchlist_id):
            response = self.agent.request(
                'GET', 'watchlists/%s' % watchlist_id)
            return response['watchlist']

        def create(self, name, *symbols):
            response = self.agent.request(
                'POST',
                'watchlists',
                params={'name': name, 'symbols': ','.join(list(symbols))})
            return response['watchlist']

        def delete(self, watchlist_id):
            response = self.agent.request(
                'DELETE', 'watchlists/%s' % watchlist_id)
            return response['watchlists']['watchlist']

    class Order():
        def __init__(self, agent) -> None:
            self.agent = agent

        def placeEquity(self, order:Order):
            response = self.agent.request('POST', 'watchlists')
            return response['watchlists']['watchlist']