FROM apache/airflow:2.7.1-python3.10

USER root
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    build-essential \
    git \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Create logs directory with proper permissions
RUN mkdir -p /opt/airflow/logs && \
    chown -R airflow:root /opt/airflow/logs && \
    chmod -R 777 /opt/airflow/logs

USER airflow
COPY requirements.txt /requirements.txt
RUN pip install -r /requirements.txt