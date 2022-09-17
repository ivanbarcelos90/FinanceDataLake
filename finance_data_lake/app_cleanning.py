from optparse import Option
import pandas as pd 
import s3_class_file as s3
import os, io
from spark_class_file import spark_session
from pyspark.sql.functions import year, month, dayofmonth 

bronze_bucket = 'finance-data-lake-bronze'
silver_bucket = 'finance-data-lake-silver'
folder = 'stock_data/'

def run():

    cleanning_data(bronze_bucket, s3.create_s3_session())
  
    # s3.upload_file(cleanned_data, silver_bucket, s3.create_s3_session())

    # os.remove(cleanned_data)
    
# Spark Method

def cleanning_data(bucket:str, s3_dict:dict):

    print('Download object from s3 bucket... \n')

    if file_path := s3.get_daily_file(bucket, folder, s3.create_s3_session()):
        spark = spark_session()
        stock_data_df = spark.read.parquet('s3a://finance-data-lake-bronze/' + file_path)    

        print('Dataframe created succefully from s3 object! \n')
        print('Starting cleanning proccess... \n')

        df_clean = stock_data_df.na.drop()

        print('Cleanning proccess completed succeffully! \n')  
        
        parquet_file_path = f's3a://{silver_bucket}/stock_data/'

        df_clean_2 = (df_clean.withColumn('year', year('Date'))
                              .withColumn('month', month('Date'))
                              .withColumn('day', dayofmonth('Date'))) 

        stock_data_df = spark.read.parquet(parquet_file_path).select('year', 'month', 'day').distinct()
        df_clean_3 = df_clean_2.join(stock_data_df, ['year', 'month', 'day'], 'leftanti')

        columns = [x.lower() for x in df_clean_3.columns]

        (df_clean_3.toDF(*columns)
                   .write
                   .parquet(parquet_file_path,
                            mode='append',
                            partitionBy=['year', 'month', 'day'],
                            compression='gzip')) 
        
        print(f'The parquet stock file {parquet_file_path} was created succefully! \n')

    else:
        print('File Not Found')

# Pandas Method

# def cleanning_data(bucket:str, s3_dict:dict):

#     print('Download object from s3 bucket... \n')

#     file_path = s3.get_daily_file(bucket, folder, s3.create_s3_session())  

#     obj = s3_dict["client"].get_object(Bucket=bucket, Key=file_path)
#     df = pd.read_parquet(io.BytesIO(obj['Body'].read()))

#     print('Dataframe created succefully from s3 object! \n')
#     print('Starting cleanning proccess... \n')

#     df_clean = df.dropna()
#     df_clean = df_clean.reset_index(drop=True)
#     df_clean[["Date", "Event"]] = df_clean[["Date", "Event"]].apply(pd.to_datetime)

#     print('Cleanning proccess completed succeffully! \n')   
#     parquet_file_path = file_path[:-8] + '.parquet'

#     df_clean.to_parquet(parquet_file_path, index=False, compression="gzip") 

#     print(f'The parquet stock file {parquet_file_path} was created succefully! \n')

#     return parquet_file_path