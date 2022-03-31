import yfinance as yf
import pandas as pd
from pathlib import Path
from os.path import abspath
from datetime import datetime


def create_ticker_df(ticker:str, prd:str = '1d', intv:str = '1d') -> pd.DataFrame:
    """_summary_

    Args:
        ticker (str): _description_
        prd (str, optional): _description_. Defaults to '1d'.
        intv (str, optional): _description_. Defaults to '1d'.

    Returns:
        pd.DataFrame: _description_
    """

    data = yf.download(ticker, group_by="Ticker", period=prd, interval=intv)
    data['ticker'] = ticker  # add this column because the dataframe doesn't contain a column with the ticker
    data['Event'] = datetime.now() 
    data.reset_index(inplace=True)   
    return data

def import_daily_stock(tickerStrings):

    gen = (create_ticker_df(t) for t in tickerStrings)     

    df = pd.concat(gen)

    df.to_csv(abspath(f'./Investigações/Stock_Data/{datetime.now().strftime("%Y_%m_%d_%H%M%S")}_stock_all.csv'), index=False)  

# Send Every Ticker Symbol to df
# Csv stock symbol file source: https://www.nasdaq.com/market-activity/stocks/screener
p = Path(abspath('./Investigações/Stock_List/Stock_Symbol.csv'))

# Create a dataframe to store all stocks symbols
symbol = pd.read_csv(p, nrows=20) # nrows got 8188 symbols

# Parameters to iterate all tickers a store all data in separate csv.
# tickerStrings = ['AAPL', 'MSFT'] # Test symbol
tickerStrings = symbol['Symbol'] # All symbols

import_daily_stock(tickerStrings)