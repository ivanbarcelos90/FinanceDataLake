import boto3, re, io
import aws_access_keys as keys
from datetime import datetime
import pandas as pd


AWS_REGION = 'us-east-1'
# AWS_PROFILE = 'localstack'
ENDPOINT_URL = 'http://localstack:4566'

def create_s3_session(aws_region:str=AWS_REGION, endpoint_url:str=ENDPOINT_URL):

    # s3 client creation
    s3_client = boto3.client("s3"
                            ,aws_access_key_id=keys.aws_access_key_id 
                            ,aws_secret_access_key=keys.aws_secret_access_key
                            ,region_name=aws_region
                            ,endpoint_url=endpoint_url)

    # Amazon S3 Resource
    s3 = boto3.resource('s3'
                        ,aws_access_key_id=keys.aws_access_key_id 
                        ,aws_secret_access_key=keys.aws_secret_access_key
                        ,region_name=aws_region
                        ,endpoint_url=endpoint_url)

    return {"client": s3_client, "resource": s3}


# Upload a new file
def upload_file(file:str, bucket:str, s3_dict:dict):
    data = open(file, 'rb') 
    data_lake_path = re.sub('/workspace/', '', file)
    s3_dict["resource"].Bucket(bucket).put_object(Key=data_lake_path, Body=data) 

    return print(f'The file {data_lake_path} was uploaded to the {bucket}')

# Read the daily file at s3
def get_daily_file(bucket:str, folder:str, s3_dict:dict):

    #Get the last from bucket
    get_last_modified = lambda obj: int(obj['LastModified'].strftime('%s'))   
    objs = s3_dict["client"].list_objects_v2(Bucket=bucket, Prefix=datetime.now().strftime(f'{folder}year=%Y/month=%m/day=%d/')).get('Contents', {})    
    last_added = [obj['Key'] for obj in sorted(objs, key=get_last_modified, reverse=True)][0]

    return last_added  

# Read all the files in a bucket
def get_all_files(bucket:str, folder:str, s3_dict:dict):

    objs = s3_dict["client"].list_objects_v2(Bucket=bucket, Prefix=folder)['Contents']  
    keys = [obj['Key'] for obj in objs]
            
    return keys