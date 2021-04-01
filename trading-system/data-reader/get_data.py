import requests
import csv
import json
from collections import OrderedDict

from base import ClientBase
import utils

from exceptions import OutOfTokensException


class DataFetcher(ClientBase):


    def __init__(selfkwargs):
        super().__init__()


    def api_usage_info(self):
        """
        Returns the current usage data based on the current API token.
        """
        return self._get_api_info()


    def fetch_ticker_catalog(self, assetTypes=[]):
        """
        Returns a list of all the tickers supported.
        params:
        - assetTypes: list to filter the types of tickers getting returned
            options: 'Stock', 'ETF', 'Mutual Fund' returns all of them if no parameter specified.
        """

        listing_url = "https://apimedia.tiingo.com/docs/tiingo/daily/supported_tickers.zip"
        res = requests.get(listing_url)

        zipfile = utils.get_zipfile(res)
        raw_csv = utils.get_buffer_from_zip(zipfile, 'supported_tickers.csv')

        reader = csv.DictReader(raw_csv)

        if not len(assetTypes):
            return [json.dumps(row) for row in reader]

        assetTypesSet = set(assetTypes)
        return [json.dumps(row) for row in reader
                if row.get('assetType') in assetTypesSet]


    def fetch_metadata(self, ticker, format='json'):
        """
        Returns the metadata for a given ticker.
        """
        try:
            res = self._make_request("daily/{0}".format(ticker))
        except (OutOfTokensException):
            # Let the user know that tiingo ran out of tokens to use and switch to the safety net data provider.
            print("NO TOKENS LEFT !!")
            return None

        if format == 'json':
            return res.json()
        elif format == 'csv':
            pass

    def fetch_latest_price(self, ticker, format='json'):
        """
        Returns the latest price about a given ticker.
        """
        try:
            res = self._make_request("daily/{0}/prices".format(ticker))
        except (OutOfTokensException):
            # Let the user know that tiingo ran out of tokens to use and switch to the safety net data provider.

            print("NO TOKENS LEFT !!")
            return None

        if format == 'json':
            return res.json()
        elif format == 'csv':
            pass

    def fetch_current_price(self, ticker):

        return self._retrieve_current_price(ticker)


    def fetch_historic_prices(self, ticker, start="1900-1-1", end="2100-1-1", format='json'):
        """
        Returns the historic prices for a given ticker, if no param specified gets the full range from stock startDate to endDate
        """
        try:
            res = self._make_request("daily/{0}{1}".format(ticker, "/prices?startDate={0}&endDate={1}".format(start, end)))
        except (OutOfTokensException):
            # Let the user know that tiingo ran out of tokens to use and switch to the safety net data provider.
            print("NO TOKENS LEFT !!")
            return None

        if format == 'json':
            return res.json()
        elif format == 'csv':
            pass

    def fetch_option_chain(self, ticker, date=None):
        return self._retrieve_option_chain(ticker, date)

    def fetch_option_dates(self, ticker):
        return self._retrieve_option_dates(ticker)

    def fetch_recommendations(self, ticker):
        return self._retrieve_recommendations(ticker)

    def fetch_holder_info(self, ticker):
        return self._retrieve_holder_info(ticker)

    def fetch_instituional_holders(self, ticker):
        return self._retrieve_instituional_holders(ticker)

    def fetch_sustainability_info(self, ticker):
        return self._retrieve_sustainability_info(ticker)

    def fetch_isin(self, ticker):
        return self._retrieve_isin(ticker)




def main():
    cl = DataFetcher()

    ticker = "AAPL"

    # Uncomment to fetch all the supported tickers.
    #print(cl.fetch_ticker_catalog())

    # Uncomment to fetch the meta data for the given ticker
    print(cl.fetch_metadata(ticker))

    # # Uncomment to fetch the current price for the given ticker
    # print(cl.fetch_latest_price(ticker))

    # Uncomment to fetch all historic prices for a given ticker
    # print(cl.fetch_historic_prices(ticker))



if __name__ == "__main__":
    main()

