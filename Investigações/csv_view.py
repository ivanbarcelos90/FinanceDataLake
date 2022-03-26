import pandas as pd
from os.path import abspath


path = abspath('./Investigações/Stock_Data/2022_03_19_195156_stock_all.csv')

csv = pd.read_csv(path)

print(csv)