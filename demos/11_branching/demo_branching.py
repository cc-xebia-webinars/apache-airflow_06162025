from datetime import datetime
from typing import Any

from airflow import DAG
from airflow.providers.standard.operators.empty import EmptyOperator
from airflow.providers.standard.operators.python import (
    BranchPythonOperator,
    PythonOperator,
)


# Function to choose which branch to follow based on the execution date
def choose_branch(**kwargs: Any) -> str:
    # If the day of the month is even, return the task_id for the even day task
    if kwargs["execution_date"].day % 2 == 0:
        return "even_day_task"
    # Otherwise, return the task_id for the odd day task
    else:
        return "odd_day_task"


# Function to print a message for even days
def print_even_day() -> None:
    print("This is an even day.")


# Function to print a message for odd days
def print_odd_day() -> None:
    print("This is an odd day.")


# Default arguments for the DAG
default_args = {
    "owner": "airflow",  # Owner of the DAG
    "start_date": datetime(2025, 2, 25),  # Start date of the DAG
}

# Define the DAG
with DAG(
    dag_id="demo_branching",  # Unique identifier for the DAG
    default_args=default_args,  # Default arguments for the DAG
    schedule="@daily",  # Schedule interval for the DAG
) as dag:
    # Define the start task
    start = EmptyOperator(task_id="start")

    # Define the branching task
    branching = BranchPythonOperator(
        task_id="branching",  # Unique identifier for the branching task
        python_callable=choose_branch,  # Function to determine which branch to follow
    )

    # Define the task for even days
    even_day_task = PythonOperator(
        task_id="even_day_task",  # Unique identifier for the even day task
        python_callable=print_even_day,  # Function to execute for even days
    )

    # Define the task for odd days
    odd_day_task = PythonOperator(
        task_id="odd_day_task",  # Unique identifier for the odd day task
        python_callable=print_odd_day,  # Function to execute for odd days
    )

    # Define the end task
    end = EmptyOperator(
        task_id="end",  # Unique identifier for the end task
        trigger_rule="none_failed_min_one_success",  # Trigger rule for the end task
    )

    # Set the task dependencies
    start >> branching  # Start task followed by branching task
    branching >> even_day_task >> end  # Even day task followed by end task
    branching >> odd_day_task >> end  # Odd day task followed by end task
