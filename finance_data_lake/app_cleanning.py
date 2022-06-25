import pandas as pd 
import s3_class_file as s3
import os, io

raw_bucket = 'finance-data-lake-raw'
data_lake_bucket = 'finance-data-lake'
folder = '/workspace/stock_data/'

def run():

    c = cleanning_data(raw_bucket, s3.create_s3_session())
  
    s3.upload_file(c, data_lake_bucket, s3.create_s3_session())

    os.remove(c)
    

def cleanning_data(bucket:str, s3_dict:dict):

    print('Download object from s3 bucket... \n')

    file_path = s3.get_daily_file(bucket, folder, s3.create_s3_session())  

    obj = s3_dict["client"].get_object(Bucket=bucket, Key=file_path)
    df = pd.read_csv(io.BytesIO(obj['Body'].read()))

    print('Dataframe created succefully from s3 object! \n')
    print('Starting cleanning proccess... \n')

    df_clean = df.dropna()
    df_clean = df_clean.reset_index(drop=True)
    df_clean[["Date", "Event"]] = df_clean[["Date", "Event"]].apply(pd.to_datetime)

    print('Cleanning proccess completed succeffully! \n')   
    parquet_file_path = file_path[:-4] + '.parquet'

    df_clean.to_parquet(parquet_file_path, index=False) 

    print('The csv stock file was created succefully! \n')

    return parquet_file_path
