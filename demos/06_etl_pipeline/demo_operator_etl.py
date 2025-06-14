from datetime import datetime
from typing import Any

from airflow import DAG
from airflow.providers.standard.operators.python import PythonOperator


# Extract step: returns a list of integers.
def extract_data(**context: Any) -> list[int]:
    data = [1, 2, 3]
    # Push data via XCom (implicitly done when returning a value)
    return data


# Transform step: doubles each value in the extracted data.
def transform_data(**context: Any) -> list[int]:
    # Pull data from previous task via XCom
    ti = context["ti"]
    data = ti.xcom_pull(task_ids="extract_data")
    transformed = [x * 2 for x in data]
    return transformed


# Load step: prints the transformed data.
def load_data(**context: Any) -> None:
    ti = context["ti"]
    data = ti.xcom_pull(task_ids="transform_data")
    print("Loaded data:", data)


# Default arguments for the DAG
default_args = {
    "start_date": datetime(2025, 1, 1),
}

# Define the DAG (Directed Acyclic Graph) for Airflow
with DAG(
    "demo_operator_etl",  # DAG id
    schedule=None,  # No schedule, manual trigger
    default_args=default_args,
    catchup=False,  # Do not perform backfill
) as dag_instance:
    # Task to extract data
    extract_task = PythonOperator(
        task_id="extract_data",
        python_callable=extract_data,
    )

    # Task to transform data
    transform_task = PythonOperator(
        task_id="transform_data",
        python_callable=transform_data,
    )

    # Task to load data
    load_task = PythonOperator(
        task_id="load_data",
        python_callable=load_data,
    )

    # Define task dependencies: extract -> transform -> load
    extract_task >> transform_task >> load_task
