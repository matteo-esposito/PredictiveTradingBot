import bs4 as bs
import pickle
import requests

def pull_sp500_stocks():
    resp = requests.get('https://en.wikipedia.org/wiki/List_of_S%26P_500_companies')
    soup = bs.BeautifulSoup(resp.text, 'lxml') # Changing resp to text format for bs4 to parse
    table = soup.find('table', {'class':'wikitable sortable'})
    tickers = [] # init stock tickers
    # first row ignored for the column headers
    for row in table.findAll('tr')[1:]:
        tickers.append(row.findAll('td')[0].text)
    return tickers

# TODO: create table for s&p 500 index
pull_sp500_stocks()


