import pendulum
from airflow.decorators import dag
from airflow.operators.bash import BashOperator


default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'retries': 1,
    'retry_delay': pendulum.duration(minutes=5),
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
def dbt_bash_dag():
    """
    Example of using BashOperator for running dbt
    """
    # Define the dbt run command using BashOperator
    dbt_seed_task = BashOperator(
        task_id='dbt_seed_task',
        bash_command='source $AIRFLOW_HOME/dbt_venv/bin/activate && cd /$AIRFLOW_HOME/dbt/jaffle_shop && dbt seed',
    )

    # Define the dbt run command using BashOperator
    dbt_run_task = BashOperator(
        task_id='dbt_run_task',
        bash_command='source $AIRFLOW_HOME/dbt_venv/bin/activate && cd /$AIRFLOW_HOME/dbt/jaffle_shop && dbt run',
    )

    # Define the dbt test command using BashOperator
    dbt_test_task = BashOperator(
        task_id='dbt_test_task',
        bash_command='source $AIRFLOW_HOME/dbt_venv/bin/activate && cd /$AIRFLOW_HOME/dbt/jaffle_shop && dbt test',
    )
    # Set task dependencies
    dbt_seed_task >> dbt_run_task >> dbt_test_task

dbt_bash_dag()