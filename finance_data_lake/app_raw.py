import yfinance as yf
import pandas as pd
from pathlib import Path
import os 
from datetime import datetime
import s3_class_file as s3

pd.options.mode.chained_assignment = None  # default='warn'

def run():
    bronze_bucket = 'finance-data-lake-bronze'
    
    # Send Every Ticker Symbol to df
    p = Path(os.path.abspath('./stock_list/stock_symbol.csv'))
    
    # Create a dataframe to store all stocks symbols
    symbol = pd.read_csv(p, nrows=8188) # nrows got 8188 symbols

    # Parameters to iterate all tickers a store all data in separate csv.
    # tickerStrings = ['AAPL','MSFT','TWTR','F','BBD','ITUB','VALE','NVDA','T','PBR','FB','TSLA','PFE','GM','INTC','UBER','KO','HPQ','DIS','CIG'] # Test symbol
    tickerStrings = symbol['Symbol'] # All symbols
    tickerStrings = tickerStrings.to_list()

    raw_data = import_daily_stock(tickerStrings, '1d','1d')

    print('Uploading file...')

    s3.upload_file(raw_data, bronze_bucket, s3.create_s3_session()) 

    os.remove(raw_data)

    
def import_daily_stock(tickerStrings:list(), prd:str='1d', intv:str='1d'):  

    print('Importing daily stock...')
    
    df_list = list()
    df = yf.download(tickers=tickerStrings, group_by="Ticker", period=prd, interval=intv, threads=True)

    path = os.path.abspath(f'./stock_data/year={datetime.now().strftime("%Y")}/month={datetime.now().strftime("%m")}/day={datetime.now().strftime("%d")}')
    file_name = f'{datetime.now().strftime("%Y_%m_%d_%H%M%S")}_stock_all.csv'

    full_path = path + '/' + file_name

    os.makedirs(path, exist_ok=True)

    for ticker in tickerStrings:
        df_ticker = df[ticker]
        df_ticker.loc[:,['ticker']] = ticker  
        df_ticker.loc[:,['Event']] = datetime.now()    
        df_list.append(df_ticker)
        
    df_total = pd.concat(df_list).reset_index()

    print('Creating csv file... \n')

    df_total.to_csv(full_path, index=False)  

    print('The stock file was created succefully! \n')

    return full_path
  