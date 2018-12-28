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
        # TODO: See issue #4: yahoo is deprecated
        self._api = 'yahoo'
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

    def get_create_tickers_tables(self):
        self._curr.execute("SELECT TICKER FROM SP500;")
        self._tickers = self._curr.fetchall()[0][0];

    # Delete everything in each ticker table and refill from 2000
    def drop_refill_database(self):
        start = dt.datetime(2000, 1, 1)
        end = dt.datetime.now()
        # Update SP500 date with today's date
        self._curr.execute(f"UPDATE SP500 SET date='{end.date()}';")
        print(f'Updating SP500 date to {end.date()}')
        for ticker in self._tickers:
            self._curr.execute(f'DELETE FROM "{ticker}";')
            self.insert_to_db(ticker.replace('.', '-'), start, end)

    # Use SP500 table to get last updated date and retrieve all new data and store into db
    def fill_database_from_last(self):
        self._curr.execute("SELECT DATE FROM SP500;")
        start = dt.datetime.combine(self._curr.fetchall()[0][0], dt.datetime.min.time())
        today = dt.datetime.now()
        # Update SP500 date with today's date
        self._curr.execute(f"UPDATE SP500 SET date='{today.date()}';")
        print(f'Updating SP500 date to {end.date()}')
        # Fill each ticker table
        for ticker in self._tickers:
            self.insert_to_db(ticker.replace('.', '-'), start, today)

    def insert_to_db(self, ticker, start, end):
        data = web.DataReader(ticker, self._api, start, end)
        print(f'Updating {ticker} with data from {self._api} from {start} to {end}.')
        for i in range(0, data.shape[0]):
            row = data.iloc[i]
            d = pd.to_datetime(row.name).date()
            # self._curr.execute(f"INSERT INTO \"{ticker}\" (date, open, high, low, adj_close, volume) VALUES ('{d}', {row['Open']}, {row['High']}, {row['Low']}, {row['Close']}, {row['Adj Close']}, {row['Volume']});")


