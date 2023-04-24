from datetime import datetime, timedelta
import app_raw, app_cleanning, app_gold, create_bucket, constants

# The DAG object; we'll need this to instantiate a DAG
from airflow import DAG

# Operators; we need this to operate!
from airflow.operators.python import PythonOperator

with DAG(
    'finance_data_lake',
    # These args will get passed on to each operator
    # You can override them on a per-task basis during operator initialization
    default_args={
        'depends_on_past': False,
        # 'email': ['airflow@example.com'],
        # 'email_on_failure': False,
        # 'email_on_retry': False,
        # 'retries': 1,
        # 'retry_delay': timedelta(minutes=5),
        # 'queue': 'bash_queue',
        # 'pool': 'backfill',
        # 'priority_weight': 10,
        # 'end_date': datetime(2016, 1, 1),
        # 'wait_for_downstream': False,
        # 'sla': timedelta(hours=2),
        # 'execution_timeout': timedelta(seconds=300),
        # 'on_failure_callback': some_function,
        # 'on_success_callback': some_other_function,
        # 'on_retry_callback': another_function,
        # 'sla_miss_callback': yet_another_function,
        # 'trigger_rule': 'all_success'
    },
    description='Finance Data Lake Job',
    schedule=timedelta(days=1),
    start_date=datetime(2022, 11, 12),
    catchup=False,
    tags=['Finance Data Lake'],
) as dag:

    b1 = PythonOperator(
        task_id='create_bucket',
        python_callable = create_bucket.run
    )

    t1 = PythonOperator(
        task_id='bronze_zone',
        python_callable = app_raw.run
    )

    t2 = PythonOperator(
        task_id='silver_zone',
        python_callable = app_cleanning.run
    )

    t3 = PythonOperator(
        task_id='gold_zone',
        python_callable = app_gold.run
    )   

    b1 >> t1 >> t2 >> t3
    
