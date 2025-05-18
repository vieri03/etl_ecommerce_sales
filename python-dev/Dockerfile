FROM python:3.8-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    build-essential \
    git \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements from Airflow directory
COPY requirements.txt /app/requirements.txt

# Install Python packages
RUN pip install -r requirements.txt && \
    pip install \
    jupyter \
    ipython \
    pytest \
    black \
    flake8 \
    ipdb

# Create necessary directories
RUN mkdir -p /app/dags /app/data /app/scripts /app/notebooks

# Add a convenience script for running Python with the correct PYTHONPATH
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

EXPOSE 8888

ENTRYPOINT ["/entrypoint.sh"]
CMD ["jupyter", "notebook", "--ip=0.0.0.0", "--allow-root", "--no-browser"]