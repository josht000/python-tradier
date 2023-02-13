import os
import json
import sys
import pytest
# sys.path.append('..\\tradier')
import tradier
from pprint import pprint

@pytest.fixture
def token():
    return os.environ['TRADIER_ACCESS_TOKEN']

def test_core(token):

    # c = tradier.Tradier(token, 'sandbox') # not tested or working ATM.
    c = tradier.Tradier(token, 'brokerage')

    print('\nquote --------')
    pprint(c.request('GET', 'markets/quotes', params={'symbols': 'spy'}))

    # print('balances------')
    # print(c.request('GET', 'user/balances'))
    # print('watchlist-----')
    # print c.watchlists.get('foo21')
    # print c.watchlists.delete('default')

    print('\nprofile--------')
    pprint(c.user.profile())

    print('\nbalances------')
    pprint(c.user.balances())

    #print('options---------')
    # got = c.request(
    #         'GET',
    #         'markets/options/expirations',
    #         params={'symbol': 'AAPL'})

    # pprint(json.dumps(got, sort_keys=True, indent=4, separators=(',', ': ')))

    # pprint(c.options.expirations('amrs'))
    # got = c.options.chains('amrs', '2015-09-18')
    # pprint(json.dumps(got, sort_keys=True, indent=4, separators=(',', ': ')))

if __name__=='__main__':
    test_core(os.environ['TRADIER_ACCESS_TOKEN'])