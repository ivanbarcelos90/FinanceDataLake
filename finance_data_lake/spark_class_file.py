import socket
from pyspark.sql import SparkSession
from pyspark.conf import SparkConf


def spark_session():

    localstack_ip = socket.gethostbyname('localstack')
    localstack_host = f'http://{localstack_ip}:4566'

    conf = SparkConf()
    conf.set('spark.jars.packages', 'org.apache.hadoop:hadoop-aws:3.3.3')
    conf.set('spark.hadoop.fs.s3a.aws.credentials.provider', 'org.apache.hadoop.fs.s3a.AnonymousAWSCredentialsProvider')
    conf.set('fs.s3a.endpoint', localstack_host)

    return SparkSession.builder.config(conf=conf).appName('testAccessS3').master("local[*]").getOrCreate()