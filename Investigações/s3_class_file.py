import boto3, os, logging
from botocore.exceptions import ClientError


AWS_REGION = 'ap-southeast-1'
# AWS_PROFILE = 'localstack'
ENDPOINT_URL = 'http://localhost:4566'

# s3 client creation
s3_client = boto3.client("s3"
                        ,region_name=AWS_REGION
                        ,endpoint_url=ENDPOINT_URL)

# Amazon S3 Resource
s3 = boto3.resource('s3'
                    ,region_name=AWS_REGION
                    ,endpoint_url=ENDPOINT_URL)

# Print out bucket names
def bucket_list():
    for bucket in s3.buckets.all():
        print(bucket.name)


# Create bucket
def create_bucket(bucket_name):
    try:
        response = s3_client.create_bucket(
            Bucket=bucket_name)
    except ClientError:
        print('Could not create S3 bucket locally.')
        raise
    else:
        return response


# Upload a new file
def upload_file(file, bucket):
    data = open(file, 'rb')
    s3.Bucket(bucket).put_object(Key=file, Body=data)
    return print(f'The file {file} was uploaded to the {bucket}')