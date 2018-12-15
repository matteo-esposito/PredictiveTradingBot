import pandas as pd
import pandas_datareader.data as web
import datetime as dt

start = dt.datetime(2000,1,1)
end = dt.datetime(2012, 12, 12)



df = web.DataReader('TSLA', 'yahoo', start, end)

print(df.head())

