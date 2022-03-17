import pandas as pd
from pathlib import Path
from os.path import abspath

p = Path(abspath('./Investigações/Stock_List/Stock_Symbol.csv'))

# find the files; this is a generator, not a list
files = p.glob('Stocks_*.csv')

# read the files into a dataframe
df = pd.concat([pd.read_csv(file) for file in files])

print(df)
