
import yfinance as yf
import pandas as pd
from pathlib import Path
from os.path import abspath

# Send Every Ticker Symbol to df
# Csv stock symbol file source: https://www.nasdaq.com/market-activity/stocks/screener
p = Path(abspath('./Investigações/Stock_List/Stock_Symbol.csv'))

# Create a dataframe to store all stocks symbols
symbol = pd.read_csv(p, nrows=10) # nrows got 8188 symbols

# Parameters to iterate all tickers a store all data in separate csv.
# tickerStrings = ['AAPL', 'MSFT'] # Test symbol
tickerStrings = symbol['Symbol'] # All symbols
prd = 'max'
intv = '1d'

for ticker in tickerStrings:
    data = yf.download(ticker, group_by="Ticker", period=prd, interval=intv)
    data['ticker'] = ticker  # add this column because the dataframe doesn't contain a column with the ticker
    data.to_csv(abspath(f'./Investigações/Stock_List/Stocks_{ticker}.csv'))  # Stocks_AAPL.csv for example


