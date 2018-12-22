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

    # TODO: Remove method when fill_db_from_last is implemented will update SP500 table with newest date (e.g. time.now())
    def store_ticker_ohlc(self):
        api = 'yahoo'
        # Get latest dates from entries
        start = dt.datetime(2018, 12, 18) # pull from db the date of the last data pulled
        end = dt.datetime.now() # todays date

        for ticker in self._tickers:
            # Separate date into three dolumns for future ref table should store (year/month/day/oprn/high/low/close/adj_val)
            data = web.DataReader(ticker, api, start, end)
            date = pd.to_datetime(data.index.values[0]).date()
            self._curr.execute(f"UPDATE SP500 SET date='{date}', open={data['Open'][0]}, high={data['High'][0]}, low={data['Low'][0]}, close={data['Close'][0]}, adj_close={data['Adj Close'][0]}, volume={data['Volume'][0]} WHERE ticker='{ticker}';")

    # Drop everything in database and refill from 2000
    def drop_refill_database(self):
        pass

    # Use SP500 table to get last updated date and retrieve all new data and store into db
    def fill_database_from_last(self):
        self._curr.execute("SELECT DATE FROM SP500 LIMIT 1;")
        start = dt.datetime.combine(self._curr.fetchall()[0][0], dt.datetime.min.time())
        today = dt.datetime.now()
        print(start, today)


api_scrapper = APIScrapper()
with api_scrapper as s:
    s.fill_database_from_last()
