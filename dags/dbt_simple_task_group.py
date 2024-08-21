import os
import pendulum
from airflow.decorators import dag
from airflow.models.param import Param
from airflow.operators.empty import EmptyOperator
from cosmos import DbtTaskGroup, ProjectConfig, ExecutionConfig, ProfileConfig, RenderConfig
from cosmos.profiles import PostgresUserPasswordProfileMapping
from cosmos.constants import LoadMode, TestBehavior


profile_config = ProfileConfig(
    profile_name="default",
    target_name="dev",
    profile_mapping=PostgresUserPasswordProfileMapping(
        conn_id="airflow_db",
        profile_args={"schema": "public"},
    ),
)

dbt_project_path=f"{os.environ['AIRFLOW_HOME']}/dbt/jaffle_shop"


default_args = {
    "owner": "airflow",
    'retries': 1,
    'retry_delay': pendulum.duration(minutes=5),
    'params': {
        'start_time': Param(None, type=["null", "string"], format="date", description="Start date for run", title="Start date"),
        'end_time': Param(None, type=["null", "string"], format="date", description="End date for run", title="End date"),
    }
}

@dag(
    schedule_interval="@daily",
    start_date=pendulum.datetime(2024, 7, 1),
    catchup=False,
    tags=["dbt"],
    max_active_runs=1,
    max_active_tasks=5,
    default_args=default_args
)
def dbt_simple_task_group() -> None:
    """
    Astronomer Cosmos example
    """
    pre_dbt = EmptyOperator(task_id="pre_dbt")

    dbt_group = DbtTaskGroup(
        group_id="dbt_group",
        project_config=ProjectConfig(
            dbt_project_path=dbt_project_path,
            manifest_path=f"{os.environ['AIRFLOW__COSMOS__DBT_DOCS_DIR']}/manifest.json",
            dbt_vars={
                "start_time": "{{ params.start_time if params.start_time is not none else data_interval_start }}",
                "end_time": "{{ params.end_time if params.end_time is not none else data_interval_end }}",
            },
            partial_parse=False,
        ),
        profile_config=profile_config,
        execution_config=ExecutionConfig(
            dbt_executable_path=f"{os.environ['AIRFLOW_HOME']}/dbt_venv/bin/dbt",
        ),
        render_config=RenderConfig(
            load_method=LoadMode.DBT_MANIFEST,
            # select=["tag:jaffle_shop"],
            # exclude=['path:seeds', 'config.materialized:view'],
            test_behavior=TestBehavior.AFTER_ALL,
            dbt_deps=False,
        ),
    )

    post_dbt = EmptyOperator(task_id="post_dbt")

    pre_dbt >> dbt_group >> post_dbt


dbt_simple_task_group()
