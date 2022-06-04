import boto3
from botocore.exceptions import ClientError
import aws_access_keys as keys


AWS_REGION = 'us-east-1'
# AWS_PROFILE = 'localstack'
ENDPOINT_URL = 'http://localstack:4566'

# s3 client creation
s3_client = boto3.client("s3"
                        ,aws_access_key_id=keys.aws_access_key_id 
                        ,aws_secret_access_key=keys.aws_secret_access_key
                        ,region_name=AWS_REGION
                        ,endpoint_url=ENDPOINT_URL)

# Amazon S3 Resource
s3 = boto3.resource('s3'
                    ,aws_access_key_id=keys.aws_access_key_id 
                    ,aws_secret_access_key=keys.aws_secret_access_key
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

# List files in a bucket
def list_files(bucket):

    my_bucket = s3.Bucket(bucket)

    for my_bucket_object in my_bucket.objects.all():
        print(my_bucket_object.key)

# Upload a new file
def upload_file(file, bucket):
    data = open(file, 'rb')
    s3.Bucket(bucket).put_object(Key=file, Body=data)
    return print(f'The file {file} was uploaded to the {bucket}')

# Delete a file in a bucket 
def delete_file(bucket, file):    
    s3_client.delete_object(Bucket=bucket, Key=file)
    return print(f'The file {file} was deleted from bucket {bucket}')
