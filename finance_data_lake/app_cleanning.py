import pandas as pd 
import s3_class_file as s3
import os

raw_bucket = 'finance-data-lake-raw'
data_lake_bucket = 'finance-data-lake'
folder = '/workspace/stock_data/'

def run():

    c = cleanning_data(raw_bucket)

    s3.upload_file(c, data_lake_bucket, s3.create_s3_session())

    os.remove(c)


def cleanning_data(bucket:str):

    print('Download object from s3 bucket... \n')

    csv = s3.get_daily_file(bucket, folder, s3.create_s3_session())

    access_file = 's3:/' + csv

    print('Dataframe created succefully from s3 object! \n')
    print('Starting cleanning proccess... \n')

    df = pd.read_csv(access_file)
    df_clean = df.dropna()
    df_clean = df_clean.reset_index(drop=True)
    df_clean[["Date", "Event"]] = df_clean[["Date", "Event"]].apply(pd.to_datetime)

    print('Cleanning proccess completed succeffully! \n')   
   
    df_clean.to_csv(access_file, index=False) 

    print('The csv stock file was created succefully! \n')

    return access_file
