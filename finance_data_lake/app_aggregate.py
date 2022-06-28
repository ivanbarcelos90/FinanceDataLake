import pandas as pd 
import s3_class_file as s3
import os, io

silver_bucket = 'finance-data-lake-silver'
gold_bucket = 'finance-data-lake-gold'
folder = 'stock_data/'

def run():

    final_data = aggregate_data(silver_bucket, folder, s3.create_s3_session())
  
    s3.upload_file(final_data, gold_bucket, s3.create_s3_session())

    os.remove(final_data)

def aggregate_data(bucket:str, folder:str, s3_dict:dict):

    obj_list = s3.get_all_files(bucket, folder, s3.create_s3_session())

    df_list = list()

    for key in obj_list:
        obj = s3_dict["client"].get_object(Bucket=bucket, Key=key)
        df = pd.read_parquet(io.BytesIO(obj['Body'].read()))
        df_list.append(df)
    
    df_aggregate = pd.concat(df_list)

    df_aggregate['Event'] = df_aggregate['Event'].dt.strftime('%d-%m-%Y')
    df_aggregate.reset_index(drop=True)
    df_aggregate.groupby(['Date', 'Event', 'ticker']).sum()

    df_aggregate.to_csv()

    return df_aggregate