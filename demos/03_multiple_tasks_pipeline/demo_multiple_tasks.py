from datetime import datetime

from airflow import DAG
from airflow.providers.standard.operators.python import PythonOperator


def hello_world() -> None:
    print("Hello, world!")


def goodbye_world() -> None:
    print("Goodbye, world!")


with DAG(
    "demo_multiple_tasks",
    schedule="@daily",
    default_args={
        "start_date": datetime(2025, 1, 1),
    },
) as dag:
    hello_world_task = PythonOperator(
        task_id="hello_world",
        python_callable=hello_world,
    )

    goodbye_world_task = PythonOperator(
        task_id="goodbye_world",
        python_callable=goodbye_world,
    )

    # run hello_world_task then run goodbye_world_task when running the DAG
    hello_world_task >> goodbye_world_task
