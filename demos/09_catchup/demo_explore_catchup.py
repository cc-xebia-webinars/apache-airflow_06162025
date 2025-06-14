# Import necessary modules
from datetime import datetime, timedelta

from airflow import DAG
from airflow.providers.standard.operators.python import PythonOperator


# Define a simple Python function to print a message with the current datetime
def print_message() -> None:
    print(f">>>>> explore scheduling demo: {datetime.now()} <<<<<<".upper())


# Define a function to calculate the date 10 days before the current date
def ten_days_before_today() -> datetime:
    return datetime.now() - timedelta(days=10)


# Define the DAG (Directed Acyclic Graph) for Airflow
with (
    DAG(
        "demo_explore_catchup",  # Name of the DAG
        default_args={
            "start_date": ten_days_before_today(),  # Set the start date to 10 days before today
        },
        schedule="@daily",  # Schedule the DAG to run daily
        catchup=False,  # Enable catchup to run missed tasks
    ) as dag
):
    # Define a task using PythonOperator to execute the print_message function
    print_message_task = PythonOperator(
        task_id="print_message",  # Unique identifier for the task
        python_callable=print_message,  # Specify the function to be called
    )

    # Set the task in the DAG
    print_message_task
