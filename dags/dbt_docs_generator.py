import os
import shutil
from datetime import datetime
from airflow.decorators import dag
from cosmos.operators import DbtDocsOperator
from cosmos import ProfileConfig
from cosmos.profiles import PostgresUserPasswordProfileMapping


env = os.environ['ENVIRONMENT']

# Update the PATH environment variable
dbt_path = f"{os.environ['AIRFLOW_HOME']}/dbt_venv/bin"
os.environ['PATH'] = f"{dbt_path}:{os.environ['PATH']}"


profile_config = ProfileConfig(
    profile_name="default",
    target_name="dev",
    profile_mapping=PostgresUserPasswordProfileMapping(
        conn_id="airflow_db",
        profile_args={"schema": "public"},
    ),
)


def save_docs_locally(project_dir: str, output_dir: str):
    # Ensure the output directory exists
    os.makedirs(output_dir, exist_ok=True)
    
    # Define the list of files to copy
    files_to_copy = [
        "target/index.html",
        "target/manifest.json",
        "target/graph.gpickle",
        "target/catalog.json"
    ]
    
    # Copy each file to the output directory
    for file in files_to_copy:
        src = os.path.join(project_dir, file)
        dst = os.path.join(output_dir, os.path.basename(file))
        shutil.copy2(src, dst)


@dag(
    schedule_interval="@daily",
    start_date=datetime(2023, 1, 1),
    catchup=False,
    tags=["dbt", "docs", env],
)
def dbt_docs_generator():

    generate_dbt_docs = DbtDocsOperator(
        task_id="generate_dbt_docs",
        project_dir="/opt/airflow/dbt/jaffle_shop",
        profile_config=profile_config,
        callback=lambda project_dir: save_docs_locally(project_dir, "/opt/airflow/dbt-docs"),
        env={'PATH': os.environ['PATH']}
    )

    generate_dbt_docs

dbt_docs_generator()