import s3_class_file as s3
from spark_class_file import spark_session
from pyspark.sql.functions import year, month, dayofmonth, col
from constants import SILVER_ZONE, GOLD_ZONE, PERFORMANCE_FOLDER

silver_bucket = SILVER_ZONE
gold_bucket = GOLD_ZONE

silver_folder = 'stock_data'
perfomance_folder = PERFORMANCE_FOLDER

# silver_bucket = 'finance-data-lake-silver'
# gold_bucket = 'finance-data-lake-gold'
# silver_folder = 'stock_data'
# perfomance_folder = 'stock_performance'

def run():

    gold_data(silver_bucket, silver_folder, perfomance_folder) 


def gold_data(bucket:str, silver_folder:str, gold_folder):

    print('Download all cleanned data from s3 stock data bucket... \n')
    print('Creating spark session!')


    spark = spark_session()


    print('Spark session created sucefully!')
    print('Creating source Dataframe from cleanned data!')


    df = spark.read.parquet('s3a://' + bucket + '/' + silver_folder + '/')  


    print('Dataframe created succefully from s3 object! \n')
    print('Proccessing has started... \n')


    df_performance = (df.withColumn('ratio', (col('open')) / (col('close')) * 100)
                        .select('date', 'ticker', 'open', 'close', 'ratio'))


    print('Performance KPI completed succeffully! \n')  

    
    parquet_file_path = f's3a://{gold_bucket}/{gold_folder}/'


    df_performance_2 = (df_performance.withColumn('year', year('Date'))
                                      .withColumn('month', month('Date'))
                                      .withColumn('day', dayofmonth('Date'))) 


    if parquet_file_path := s3.get_daily_file(gold_bucket, gold_folder, s3.create_s3_session()):
        stock_data_df = spark.read.parquet(parquet_file_path).select('year', 'month', 'day').distinct()
        df_performance_3 = df_performance_2.join(stock_data_df, ['year', 'month', 'day'], 'leftanti')

    else:
        df_performance_3 = df_performance_2
        parquet_file_path = f's3a://{gold_bucket}/{gold_folder}/'


    (df_performance_3.write
                    .parquet(parquet_file_path,
                                mode='append',
                                partitionBy=['year', 'month', 'day'],
                                compression='gzip')) 
                                
    
    print(f'The performance kpi file {parquet_file_path} was created succefully! \n')
