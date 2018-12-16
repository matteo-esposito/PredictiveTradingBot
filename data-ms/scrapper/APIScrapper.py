import pandas as pd
import pandas_datareader.data as web
import datetime as dt
import psycopg2

# APIScrapper class implements the exit, enter function to allow the use of with expression to close db connection when all transactions are done
class APIScrapper:
    def __init__(self):
        self._tickers = []
        self._conn = None
        self._curr = None
        print("API Scrapper initialized...")

    def __enter__(self):
        self._conn = psycopg2.connect('dbname=ModelData user=postgres password=123')
        self._curr = self._conn.cursor()
        return self

    def __exit__(self, type, value, tb):
        if tb is None:
            # No exception so commit else rollback
            self._conn.commit()
        self._curr.close()
        self._conn.close()
        self._curr = None
        self._conn = None

    def get_tickers(self):
        self._curr.execute("SELECT * FROM SP500;")
        self._tickers = [ticker[0] for ticker in self._curr.fetchall()]

    def store_ticker_ohlic(self):
        api = 'yahoo'
        # Get latest dates from entries
        start = dt.datetaime(2000, 1, 1) # temp
        end = dt.datetime(2018, 12, 12) # temp

        for ticker in self._tickers:
            # Separate date into three dolumns for future ref table should store (year/month/day/oprn/high/low/close/adj_val)
            dt = web.DataReader(ticker, api, start, end)

api_scrapper = APIScrapper()
with api_scrapper as s:
    s.get_tickers()
    print(s._tickers)



