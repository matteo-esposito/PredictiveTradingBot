import bs4 as bs
import pickle
import requests
import psycopg2

def pull_sp500_stocks():
    resp = requests.get('https://en.wikipedia.org/wiki/List_of_S%26P_500_companies')
    soup = bs.BeautifulSoup(resp.text, 'lxml') # Changing resp to text format for bs4 to parse
    table = soup.find('table', {'class':'wikitable sortable'})
    tickers = [] # init stock tickers
    # first row ignored for the column headers
    for row in table.findAll('tr')[1:]:
        tickers.append(row.findAll('td')[0].text)
    return tickers

def store_to_db(tickers):
    conn = psycopg2.connect('dbname=ModelData user=postgres password=123')
    cur = conn.cursor()

    # Drop and recreate table for updating tickers
    cur.execute("DROP TABLE SP500;")
    cur.execute("CREATE TABLE SP500 (ticker)")

     # Add to db
    for ticker in tickers:
        cur.execute(f"INSERT INTO SP500 (ticker) VALUES ('{ticker}');")
    conn.commit()
    cur.close()
    conn.close()

# This file should be called whenever there is a need to update the tickers
store_to_db(pull_sp500_stocks())

