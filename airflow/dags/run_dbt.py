# dags/dbt_warehouse_dag.py
from airflow import DAG
from airflow.operators.bash import BashOperator
from datetime import datetime, timedelta
import os

DBT_PROJECT_DIR = "/opt/airflow/dbt"

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2024, 10, 30),
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

dag = DAG(
    'dbt_warehouse_models',
    default_args=default_args,
    description='DBT warehouse transformation pipeline',
    schedule_interval= '30 * * * *',#'@hourly',
    catchup=False
)

# Run staging models first
dbt_staging = BashOperator(
    task_id='dbt_staging',
    bash_command=f'cd /opt/airflow/dbt && dbt run --models staging.*',
    dag=dag
)

# Then run marts models
dbt_marts = BashOperator(
    task_id='dbt_marts',
    bash_command=f'cd /opt/airflow/dbt && dbt run --models marts.*',
    dag=dag
)

# Finally run tests
dbt_test = BashOperator(
    task_id='dbt_test',
    bash_command=f'cd /opt/airflow/dbt && dbt test',
    dag=dag
)

# Set task dependencies
dbt_staging >> dbt_marts >> dbt_test