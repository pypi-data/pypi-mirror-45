# -*- coding: utf-8 -*-
# Standard imports
# For 2.x and 3.x compatibility
# (http://python-future.org/compatible_idioms.html)
from future.moves.urllib.request import urlopen
from future.moves.urllib.error import HTTPError

import json
import requests
from datetime import date, datetime
import time
import re
from collections import OrderedDict
import logging

# 3rd party imports
from django.core.exceptions import ImproperlyConfigured
from django.core.management.base import BaseCommand
from django.conf import settings
from django.core.cache import cache

from currency_history.models import Currency

from bs4 import BeautifulSoup

# Own imports
from ...models import Security, Price

logger = logging.getLogger(__name__)

class Command(BaseCommand):

    soup = None

    def add_arguments(self, parser):

        # Wait time between subsequent stock API calls
        parser.add_argument('-w', '--wait',
                            help='Time to wait between API calls',
                            dest='api_wait_time')

    def handle(self, *args, **options):
        securities = Security.objects.all()
        today = date.today()

        for security in securities:
            if security.price_tracker.name == 'Kauppalehti':
                quote = self.get_kauppalehti_stock_quote(security.name)
            elif security.price_tracker.name == 'GoogleFinance':
                quote = self.get_google_finance_stock_quote(security.ticker)
            elif security.price_tracker.name == 'AlphaVantage':
                AV_DELAY = getattr(settings, "ALPHA_VANTAGE_DELAY", 30)
                # If -w/--wait was given, use that value instead of settings
                if options['api_wait_time']:
                    logger.debug('api_wait_time {}'
                                 .format(options['api_wait_time']))
                    AV_DELAY = int(options['api_wait_time'])
                quote = self.get_alpha_vantage_stock_quote(security.ticker,
                                                           AV_DELAY)
            elif security.price_tracker.name == 'Yahoo':
                quote = self.get_yahoo_stock_quote(security.ticker)
            elif security.price_tracker.name == 'IEXCloud':
                quote = self.get_iexcloud_stock_quote(security.ticker)
            else:
                raise ImproperlyConfigured(
                    'Unkown price tracker {}'.format(
                        security.price_tracker.name))

            if not quote.get('price'):
                logger.debug('No ticker {} found by {}'.format(
                    security.ticker, security.price_tracker.name))
                continue
            # Update price
            Price.objects.update_or_create(date=today,
                                           security=security,
                                           defaults={
                                               'price': quote['price'],
                                               'currency': quote['currency'],
                                               'change': quote['change'],
                                               'change_percentage': quote['change_percentage']})

    def get_iexcloud_stock_quote(self, ticker_symbol):
        """
        {
        "avgTotalVolume": 1366647,
        "calculationPrice": "close",
        "change": 0.25,
        "changePercent": 0.01233,
        "close": 20.52,
        "closeTime": 1554494524181,
        "companyName": "Tanger Factory Outlet Centers, Inc.",
        "delayedPrice": 20.52,
        "delayedPriceTime": 1554494524185,
        "extendedChange": 0.06,
        "extendedChangePercent": 0.00292,
        "extendedPrice": 20.58,
        "extendedPriceTime": 1554671742673,
        "high": 20.58,
        "iexAskPrice": null,
        "iexAskSize": null,
        "iexBidPrice": null,
        "iexBidSize": null,
        "iexLastUpdated": null,
        "iexMarketPercent": null,
        "iexRealtimePrice": null,
        "iexRealtimeSize": null,
        "iexVolume": null,
        "latestPrice": 20.52,
        "latestSource": "Close",
        "latestTime": "April 5, 2019",
        "latestUpdate": 1554494524181,
        "latestVolume": 1770483,
        "low": 20.25,
        "marketCap": 1927689840,
        "open": null,
        "openTime": null,
        "peRatio": 45.78,
        "previousClose": 20.27,
        "symbol": "SKT",
        "week52High": 24.91,
        "week52Low": 19.75,
        "ytdChange": 0.01772
        }

        """

        API_KEY = getattr(settings, "IEXCLOUD_API_KEY", None)
        if not API_KEY:
            raise ImproperlyConfigured(
                'IEXCLOUD_API_KEY not set')
        url = 'https://cloud.iexapis.com/beta/stock/' + ticker_symbol + \
              '/quote?token=' + API_KEY
        response = requests.get(url)
        iexquote =  json.loads(response.content.decode('unicode_escape'),
                                 object_pairs_hook=OrderedDict)
        quote = {}
        quote['price'] = iexquote['latestPrice']
        quote['change'] = iexquote['change']
        quote['change_percentage'] = '{:.3}'.format(float(iexquote['changePercent'] * 100))
        # Doesn't support Nasdaq Helsinki, assuming USD for the currency
        currency = Currency.objects.filter(
                    iso_code='USD')[0]
        quote['currency'] = currency
        # lastest update price is in milliseconds since epoch
        # (https://iexcloud.io/docs/api/#quote)
        # Interested only in in date update was made
        latest_update = iexquote['latestUpdate'] / 1000
        latest_date = time.strftime("%Y-%m-%d",
                                    time.localtime(latest_update))
        quote['date'] = latest_date

        return quote

    def get_yahoo_stock_quote(self, ticker_symbol):
        """
        For resulting JSON,see eg.
        https://query1.finance.yahoo.com/v7/finance/chart/ASPO.HE?&interval=15m
        on browser
        """
        logger.debug('Ticker {}, using Yahoo'.format(ticker_symbol))
        if ticker_symbol == 'N/A':
            return {}

        url = 'https://query1.finance.yahoo.com/v7/finance/chart/' + \
              ticker_symbol + '?&interval=15m'
        response = requests.get(url)
        yahoo_quote = json.loads(response.content.decode('unicode_escape'),
                                 object_pairs_hook=OrderedDict)
        quote_data = yahoo_quote['chart']['result'][0]
        quote_meta = quote_data['meta']

        # Previous day close
        previous_close = quote_meta['previousClose']

        # lastest value, so far today
        latest_date_stamp = quote_data['timestamp'][-1]
        latest_date = datetime.fromtimestamp(
            latest_date_stamp).strftime(
                '%Y-%m-%d')

        # Finding out the latest price, timestamp appreast to be related to
        # quote value, and if no transactions has happened during timestamp
        # (or timestamp perido, determined by url), quote value appears to
        # be None
        quote_period = quote_data['indicators']['quote'][0]
        # Loop from end, until first non None value is found
        current_index = len(quote_period['close']) -1
        latest_price = None
        while current_index >= 0:
            if quote_period['close'][current_index] != None:
                latest_price = quote_period['close'][current_index]
                break
            else:
                current_index -= 1
        # If all the values were none, apparently no transactions during
        # the period, assuming chartPreviousClose is the latest transaction
        if latest_price == None:
            latest_price = quote_meta['previousChartClose']

        change = '{:.3}'.format(latest_price - previous_close)
        change_percentage = '{:.3}'.format(
            (latest_price - previous_close ) / previous_close * 100
        )

        period_close = quote_period['close'][-1]

        quote = {}
        quote['price'] = '{:.2f}'.format(latest_price)
        quote['change'] = change
        quote['change_percentage'] = change_percentage
        quote['date'] = latest_date

        exhange = quote_meta['exchangeName']
        if exhange == 'HEL':
            currency = Currency.objects.filter(
                iso_code='EUR')[0]
        else:
            # exhange something else that Helsinki, assume USD values
            currency = Currency.objects.filter(
                iso_code='USD')[0]

        quote['currency'] = currency

        return quote

    def get_alpha_vantage_stock_quote(self, ticker_symbol, delay=None):
        """
        "Meta Data": {
        "1. Information": "Daily Prices (open, high, low, close) and Volumes",
        "2. Symbol": "<ticker>",
        "3. Last Refreshed": "2018-05-25",
        "4. Output Size": "Compact",
        "5. Time Zone": "US/Eastern"
        },
        "Time Series (Daily)": {
            "2018-05-25": {
                "1. open": "20.6900",
                "2. high": "20.7300",
                "3. low": "20.5700",
                "4. close": "20.6900",
                "5. volume": "144404"
            },
            "2018-05-24": {
                "1. open": "20.5000",
                "2. high": "20.7200",
                "3. low": "20.4300",
                "4. close": "20.6900",
                "5. volume": "187313"
           },
        }
        """
        API_KEY = getattr(settings, "ALPHA_VANTAGE_API_KEY", None)
        if not API_KEY:
            raise ImproperlyConfigured(
                'ALPHA_VANTAGE_API_KEY not set')
        logger.debug('Ticker {}'.format(ticker_symbol))
        if ticker_symbol == 'N/A':
            return {}

        # Check if ticker recently requested
        cached = cache.get(ticker_symbol)

        url = 'https://www.alphavantage.co/query?' \
              'function=TIME_SERIES_DAILY&symbol=' + ticker_symbol + \
              '&interval=15min&apikey=' + API_KEY

        time_series = 'Time Series (Daily)'

        close_value = '4. close'

        if not cached:
            # Alpha Vantage don't want too many requests pre minute
            # (effectively only two at the moment
            if delay:
                logger.debug('AV delay {}'.format(delay))
                time.sleep(delay)

            response = requests.get(url)
            alpha_quote = json.loads(response.content.decode('unicode_escape'),
                                 object_pairs_hook=OrderedDict)
            # If request did return proper quote data, alpha_quote has key
            # name time_series. In that case, cache the result
            if time_series in alpha_quote:
                logger.debug('Caching {}'.format(ticker_symbol))
                # AlphaVantage has limited requests rate per minute, cache
                # results to avoid hitting AV servers too often.
                cache.set(ticker_symbol, alpha_quote)
        else:
            alpha_quote = cached
            logger.debug('Already cached {}'.format(ticker_symbol))
        try:
            time_series = alpha_quote[time_series]
        except KeyError:
            logger.debug('{}'.format(alpha_quote))
            # This share did not exists, or some other error occurred
            return {}
        latest_date = list(time_series.keys())[0]
        latest_value = float(time_series[latest_date][close_value])
        previous_date = list(time_series.keys())[1]
        previous_close = float(time_series[previous_date][close_value])
        change = '{:.3}'.format(latest_value - previous_close)
        change_percentage = '{:.3}'.format(
            (latest_value - previous_close ) / previous_close * 100
        )
        quote = {}
        quote['price'] = '{:.2f}'.format(latest_value)
        quote['change'] = change

        quote['change_percentage'] = change_percentage
        quote['date'] = latest_date
        # if the ticker is in format 'TICKER.EXHANGE'
        if ticker_symbol.rpartition('.')[1] == '.':
            exhange = ticker_symbol.rpartition('.')[-1]
            if exhange == 'HE':
                currency = Currency.objects.filter(
                    iso_code='EUR')[0]
            else:
                # exhange something else that Helsinki, assume USD values
                currency = Currency.objects.filter(
                    iso_code='USD')[0]
        else:
            # No dot found in ticker symbol, assume US market with USD
            currency = Currency.objects.filter(
                iso_code='USD')[0]
        quote['currency'] = currency

        return quote

    def get_google_finance_stock_quote(self, ticker_symbol):
        """
        """

        url = 'https://finance.google.com/finance?output=json&q=%s' % ticker_symbol
        response = requests.get(url)
        if response.status_code == 200:
            # This magic here is to cut out various leading characters from
            # the JSON response, as well as trailing stuff (a terminating
            # ']\n' sequence), and then we decode the escape sequences in
            # the response This then allows you to load the resulting
            # string with the JSON module.
            try:
                google_quote = json.loads(response.content[6:-2] \
                                          .decode('unicode_escape'))
            except ValueError:
                # The response does not start with b'\n// [\n{...', so it is
                # assumed that the query returned no matches, maybe something
                # like
                # b'\n{\n"start" : "",\n"num" : "",\n"num_company_results" :
                # "0",\n"num_mf_results" : "0",\n"num_all_results" : 
                # Return empty dictionary
                return {}
        else:
            # Something else was returned as response code than 200
            return {}

        quote = {}
        quote['price'] = google_quote['l']
        quote['change'] = google_quote['c'] or '0.0'
        quote['change_percentage'] = google_quote['cp'] or '0.0'

        # Get the currency, all stocks in Helsinki are expected to be in euros
        if google_quote['exchange'] == 'HEL':
            currency = Currency.objects.filter(
                iso_code='EUR')[0]
        else:
            currency = Currency.objects.filter(
                iso_code='USD')[0]
        quote['currency'] = currency
        return quote

    def get_kauppalehti_stock_quote(self, security_name):
        """
        Fetch stock quotes from Kauppalehti, by scraping the web page, as
        there's no API to get a quote for a single stock
        """

        quote = {}
        # Url to scrape
        url = "http://www.kauppalehti.fi/5/i/porssi/porssikurssit/lista.jsp?reverse=false&gics=kaikki&psize=300&rdc=117c1f2c2b5&currency=euro&listIds=kaikki&order=alpha&markets=XHEL"

        # Only fetch the web-page once
        if not self.soup:
            stock_page = urlopen(url)
            self.soup = BeautifulSoup(stock_page)

        # At the moment, 7th table has is the one with stock data
        table = self.soup('table')[6]

        # All prices are in Euros
        currency_euro = Currency.objects.filter(
            iso_code='EUR')[0]
        quote['currency'] = currency_euro

        for row in table.findAll('tr'):
            cells = row('td')

            # The table has headers inside <td>, but no need to worry about
            # them
            # First cell has the name of the stock
            if cells[0].a is not None:
                # Find the value inside <td> </td>
                if security_name == cells[0].a.string:
                    # Second cell has the current value of the stock
                    if cells[1] is not None:
                        quote['price'] = cells[1].string

                    # Change %
                    # Change percentage has '%' char at the end, remove it
                    # and convert  it to float. KL marks 'no change' as '-'
                    if cells[2].string == '-':
                        change_percentage = 0
                    else:
                        change_percentage = float(re.sub('[%]',
                                                         '',
                                                         cells[2].string))
                    # KL does not offer change in euros, need to calculate
                    current_value = float(cells[1].string)
                    previous_close = (current_value * 100) / (100 + change_percentage)
                    change = current_value - previous_close
                    quote['change'] = change
                    quote['change_percentage'] = change_percentage

        return quote
