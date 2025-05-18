import subprocess
from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python import PythonOperator

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 3,
    'retry_delay': timedelta(minutes=5),
}

def run_etl_script(**context):
    try:
        result = subprocess.run(
            ['python3', '/opt/airflow/dags/scripts/etl.py'],
            check=True,  # Will raise CalledProcessError if exit code != 0
            capture_output=True,
            text=True
        )
        print("STDOUT:", result.stdout)
        print("STDERR:", result.stderr)
    except subprocess.CalledProcessError as e:
        print("ETL script failed with exit code", e.returncode)
        print("Output:", e.output)
        print("Error:", e.stderr)
        raise  # Let Airflow mark the task as failed

# Define DAG
dag = DAG(
    'dag_ecommerce',
    default_args=default_args,
    description='ETL pipeline for ingesting data from CSV to ClickHouse',
    schedule_interval='@hourly',
    start_date=datetime(2025, 5, 18),
    catchup=False,
    max_active_runs=1
)

# Define Task
ingest_task = PythonOperator(
    task_id='run_etl_script',
    python_callable=run_etl_script,
    dag=dag
)
