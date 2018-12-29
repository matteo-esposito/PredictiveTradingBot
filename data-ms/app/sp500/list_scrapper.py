import bs4 as bs
import pickle
import requests
import psycopg2
import datetime as dt

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
    conn = psycopg2.connect('dbname=postgres user=postgres password=123 host=postgres')
    cur = conn.cursor()

    cur.execute("CREATE TABLE SP500 (ticker text[], date date);")

    tickers = list(map(str, tickers))
    # Add to db
    stm = f"INSERT INTO SP500 (ticker, date) VALUES (%s, '{dt.datetime.now().date()}');"
    cur.execute(stm, (tickers, ))

    for ticker in tickers:
        cur.execute(f'CREATE TABLE "{ticker}" (date date, open decimal, high decimal, low decimal, close decimal, adj_close decimal, volume integer);')

    conn.commit()
    cur.close()
    conn.close()

