import yfinance as yf
import pandas as pd
from pathlib import Path
from os.path import abspath
from datetime import datetime

# Send Every Ticker Symbol to df
# Csv stock symbol file source: https://www.nasdaq.com/market-activity/stocks/screener
p = Path(abspath('./Investigações/Stock_List/Stock_Symbol.csv'))

# Create a dataframe to store all stocks symbols
symbol = pd.read_csv(p, nrows=8188) # nrows got 8188 symbols

# Parameters to iterate all tickers a store all data in separate csv.
# tickerStrings = ['AAPL', 'MSFT'] # Test symbol
tickerStrings = symbol['Symbol'] # All symbols

prd = '1d'
intv = '1d'
df = pd.DataFrame()
for ticker in tickerStrings:
    data = yf.download(ticker, group_by="Ticker", period=prd, interval=intv)
    data['ticker'] = ticker  # add this column because the dataframe doesn't contain a column with the ticker
    data['Event'] = datetime.now()
    data.reset_index(inplace=True) 
    # df = df.append(data)
    df = [df for df in data]

df.to_csv(abspath(f'./Investigações/Stock_Data/{datetime.now().strftime("%Y_%m_%d_%H%M%S")}_stock_all.csv'), index=False)  
      