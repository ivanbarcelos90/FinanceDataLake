import yfinance as yf
import pandas as pd
from pathlib import Path
from os.path import abspath
from datetime import datetime

def import_daily_stock(ticker:list(), prd:str='1d', intv:str='1d'):

    df_list = list()
    df = yf.download(tickers=tickerStrings, group_by="Ticker", period=prd, interval=intv, threads=True)

    for ticker in tickerStrings:
        df_ticker = df[ticker]
        df_ticker['ticker'] = ticker  
        df_ticker['Event'] = datetime.now()    
        df_list.append(df_ticker)
        
    df_total = pd.concat(df_list).reset_index()
    df_total.to_csv(abspath(f'./Investigações/Stock_Data/{datetime.now().strftime("%Y_%m_%d_%H%M%S")}_stock_all.csv'), index=False)  
           
# Send Every Ticker Symbol to df
# Csv stock symbol file source: https://www.nasdaq.com/market-activity/stocks/screener
p = Path(abspath('./Investigações/Stock_List/Stock_Symbol.csv'))

# Create a dataframe to store all stocks symbols
symbol = pd.read_csv(p, nrows=8188) # nrows got 8188 symbols

# Parameters to iterate all tickers a store all data in separate csv.
# tickerStrings = ['AAPL','MSFT','TWTR','F','BBD','ITUB','VALE','NVDA','T','PBR','FB','TSLA','PFE','GM','INTC','UBER','KO','HPQ','DIS','CIG'] # Test symbol
tickerStrings = symbol['Symbol'] # All symbols
tickerStrings = tickerStrings.to_list()

import_daily_stock(tickerStrings, '1d','1d')
    