import pandas as pd 
import s3_class_file as s3
import os, io
from datetime import datetime

silver_bucket = 'finance-data-lake-silver'
gold_bucket = 'finance-data-lake-gold'
folder = 'stock_data/'

def run():

    final_data = aggregate_data(silver_bucket, folder, s3.create_s3_session())
  
    s3.upload_file(final_data, gold_bucket, s3.create_s3_session())

    # os.remove(final_data)

def aggregate_data(bucket:str, folder:str, s3_dict:dict):

    print('Download object from s3 bucket... \n')

    obj_list = s3.get_all_files(bucket, folder, s3.create_s3_session())

    df_list = list()

    for key in obj_list:
        obj = s3_dict["client"].get_object(Bucket=bucket, Key=key)
        df = pd.read_parquet(io.BytesIO(obj['Body'].read()))
        df_list.append(df)
    
    df_aggregate = pd.concat(df_list)

    print('Dataframe created succefully from s3 object! \n')
    print('Starting aggregate proccess... \n')

    df_aggregate['Event'] = df_aggregate['Event'].dt.strftime('%Y-%m')
    df_aggregate['Date'] = df_aggregate['Date'].dt.strftime('%Y-%m')
    df_aggregate.reset_index(drop=True)
    df_aggregate.groupby(['Date', 'Event', 'ticker']).sum()

    print('Aggregate proccess completed succeffully! \n') 

    gold_path = os.path.abspath(f'./stock_data_monthly/year={datetime.now().strftime("%Y")}/month={datetime.now().strftime("%m")}')
    os.makedirs(gold_path, exist_ok=True)

    full_path = gold_path + '/stock_all.csv' 

    df_aggregate.to_csv(full_path, index=False)

    print(f'The parquet stock file {full_path} was created succefully! \n')

    return full_path
