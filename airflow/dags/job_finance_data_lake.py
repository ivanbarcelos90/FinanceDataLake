
from pathlib import Path
import sys, os
from datetime import datetime, timedelta
from textwrap import dedent


posix_path = Path(__file__).parents[2].absolute()
app_path = os.path.join(str(posix_path), 'finance_data_lake')
sys.path.insert(0, app_path)

import app_raw

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
    start_date=datetime(2022, 11, 4),
    catchup=False,
    tags=['Finance Data Lake'],
) as dag:

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
    
    t1.doc_md = dedent(
        """
    #### Task Documentation
    A working job to run the Finance Data Lake
    """
    )

    dag.doc_md = __doc__  # providing that you have a docstring at the beginning of the DAG; OR
    dag.doc_md = """
    This is a documentation placed anywhere
    """  # otherwise, type it like this
    templated_command = dedent(
    """
    A working job to run the Finance Data Lake  
    """
    )

    t1 >> t2 >> t3
