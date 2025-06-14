from datetime import datetime
from typing import Any

from airflow import DAG
from airflow.providers.standard.operators.python import PythonOperator


# This function returns a greeting string using the provided subject.
def get_greeting(subject: str) -> str:
    return f"Hello, {subject}!"


# This function pulls the greeting from XCom and prints it.
def print_greeting(**context: Any) -> None:
    ti = context["ti"]  # TaskInstance object from context
    greeting = ti.xcom_pull(
        task_ids="get_greeting"
    )  # Pulls XCom pushed by get_greeting
    print(greeting)  # Prints the greeting


# Define the DAG (Directed Acyclic Graph) for Airflow
with DAG(
    "task_params",  # DAG id
    schedule="@daily",  # Run daily
    default_args={
        "start_date": datetime(2025, 1, 1),  # Start date for the DAG
    },
) as dag:
    # Task to get the greeting string with a parameter
    get_greeting_task = PythonOperator(
        task_id="get_greeting",
        python_callable=get_greeting,
        op_args=["John"],  # Pass the subject here
    )

    # Task to print the greeting string
    print_greeting_task = PythonOperator(
        task_id="print_greeting",
        python_callable=print_greeting,
    )

    # Set task dependencies: get_greeting_task runs before print_greeting_task
    get_greeting_task >> print_greeting_task
