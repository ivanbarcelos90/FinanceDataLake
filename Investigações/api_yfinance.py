
import yfinance as yf
import pandas as pd
from pathlib import Path
from os.path import abspath
from os import mkdir
import sqlite3

# Send Every Ticker Symbol to df
# Csv stock symbol file source: https://www.nasdaq.com/market-activity/stocks/screener
p = Path(abspath('./Investigações/Stock_List/Stock_Symbol.csv'))

# Create a dataframe to store all stocks symbols
# symbol = pd.read_csv(p, nrows=10) # nrows got 8188 symbols

# Parameters to iterate all tickers a store all data in separate csv.
tickerStrings = ['AAPL', 'MSFT'] # Test symbol
# tickerStrings = symbol['Symbol'] # All symbols
prd = 'max'
intv = '1d'
df = pd.DataFrame()
for ticker in tickerStrings:
    data = yf.download(ticker, group_by="Ticker", period=prd, interval=intv)
    data['ticker'] = ticker  # add this column because the dataframe doesn't contain a column with the ticker
    data.reset_index(inplace=True) 
    df = df.append(data)

rows = df.shape[0]


# Create connection.
cnx = sqlite3.connect('Data.db')
df.to_sql(name='Stock', if_exists='replace', con=cnx)

param = {'2022-03-18'}
query = pd.read_sql('select * from Stock where Date = ?', cnx, params=param)
# query.Date = pd.to_datetime(query.Date)
print(query)

# for i in range(rows + 1):      
#     if not abspath(f'./Investigações/Stock_Data/{data.iloc[i,0]}'):
#         mkdir(abspath(f'./Investigações/Stock_Data/{data.iloc[i,0]}'))  
      

cnx.close()