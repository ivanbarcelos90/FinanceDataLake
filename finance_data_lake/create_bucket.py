import s3_class_file as s3
from constants import BRONZE_ZONE, SILVER_ZONE, GOLD_ZONE
from airflow.models import Variable


def run():

    s3.create_bucket(BRONZE_ZONE, s3.create_s3_session())
    s3.create_bucket(SILVER_ZONE, s3.create_s3_session())
    s3.create_bucket(GOLD_ZONE, s3.create_s3_session())
    