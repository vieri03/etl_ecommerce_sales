# Development and Optimization of an ETL Pipeline for E-commerce Sales Data

#### Author: Gabriel Vieri

This document outlines the ETL (Extract, Transform, Load) process designed to ingest and transform data from raw source files into a structured format within the data warehouse. It includes details on data sources, transformation logic, pipeline architecture, and the final schema in the data warehouse.


### Data Pipeline Architecture


### Data Sources

| Source Name | Type      |  Location                               |
| ----------- | --------- |  ---------------------------------------|
| Sales       | CSV file  |  /data/E-commerece sales data 2024.csv  |
| Customers   | CSV file  |  /data/customer_details.csv             |
| Products    | CSV file  |  /data/product_details.csv              |

### Preprocessing Logic
- Standardize column names
- Convert date strings to standard format datetimes
- Convert numerical strings to integers/floats
- Fill missing values where applicable

### Transformation Logic


### Airflow DAG Configuration
1. DAG Name: dag_ecommerce
    - Schedule: @hourly
    - Retry Policy: 3 retries with 5-minute delay
    - Task: ingest_data (calls etl.py)
2. DAG Name: dbt_warehouse_models
    - Schedule: 30 * * * *
    - Retry Policy: 1 retries with 5-minute delay
    - Task: dbt_staging >> dbt_marts >> dbt_test


### Testing & Monitoring
- Docker healthchecks for PostgreSQL availability
- Logging via Airflow task logs
- Manual test run using:
docker exec -it airflow-worker python /opt/airflow/dags/scripts/etl.py

### Notes
ETL can be re-run without duplicate inserts (uses truncates tables)

### Docker Compose Stack

### Services Overview
postgres: Metadata store for Airflow
clickhouse: Database to store ingested data and behaves as analytics databases
airflow-webserver: UI for managing DAGs and tasks
airflow-scheduler: Triggers tasks at scheduled intervals
python-dev: Jupyter Notebook for development purposes inside Docker

### Volumes
- postgres_data: Stores PostgreSQL database files
- airflow_logs: Stores Airflow task logs 
- clickhouse_data: Stores database files for data warehouse
- ./airflow/dags: Stores DAG definitions and scripts
- ./data: Stores source data
- ./python-dev/: Stores testing script for Jupyter Notebook
- ./dbt: Stores dbt configuration

### Startup Commands
docker-compose up -d --build