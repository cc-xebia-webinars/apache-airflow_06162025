from datetime import datetime

from airflow.decorators import dag, task


# Extract step: returns a list of integers.
@task
def extract_data() -> list[int]:
    data = [1, 2, 3]
    return data


# Transform step: doubles each value in the extracted data.
@task
def transform_data(data: list[int]) -> list[int]:
    transformed = [x * 2 for x in data]
    return transformed


# Load step: prints the transformed data.
@task
def load_data(data: list[int]) -> None:
    print("Loaded data:", data)


# Default arguments for the DAG
default_args = {
    "start_date": datetime(2025, 1, 1),
}


# Define the DAG using the TaskFlow API
@dag(
    schedule="@daily",  # Run daily
    default_args=default_args,  # Default arguments
    catchup=False,  # Do not perform backfill
)
def demo_task_flow_etl():
    # Define the ETL workflow using task dependencies
    data = extract_data()  # Extract step
    transformed_data = transform_data(data)  # Transform step
    load_data(transformed_data)  # Load step


# Instantiate the DAG
dag_instance = demo_task_flow_etl()
