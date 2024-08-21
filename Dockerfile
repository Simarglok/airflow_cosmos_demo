FROM apache/airflow:2.9.2-python3.12
USER root
RUN apt-get update -y \
 && apt-get install -y git \
 && apt-get clean \
 && rm -rf /var/lib/apt/lists/*
USER airflow
COPY requirements.txt /
RUN pip install --no-cache-dir -r /requirements.txt

USER root
COPY requirements_dbt_venv.txt /tmp/
# install dbt into a virtual environment
RUN python -m venv dbt_venv && source dbt_venv/bin/activate && \
    pip install --no-cache-dir --no-user -r /tmp/requirements_dbt_venv.txt && deactivate