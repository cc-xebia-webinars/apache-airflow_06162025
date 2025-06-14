from datetime import datetime
from typing import Any, Mapping

from airflow.decorators import dag, task
from airflow.providers.standard.operators.empty import EmptyOperator
from airflow.providers.standard.operators.python import get_current_context


# Define the DAG using the @dag decorator
@dag(
    dag_id="demo_branching_task_flow",  # Unique identifier for the DAG
    default_args={
        "owner": "airflow",
        "start_date": datetime(2025, 3, 2),
    },  # Default arguments for the DAG
    schedule="@daily",  # Schedule interval for the DAG
)
def demo_branching() -> None:
    # Define the start task using the EmptyOperator
    start = EmptyOperator(task_id="start")

    # Define a branching task using the @task.branch decorator
    @task.branch
    def choose_branch() -> str:
        context: Mapping[str, Any] = get_current_context()
        execution_date: datetime = context["execution_date"]
        if execution_date.day % 2 == 0:
            return "print_even_day"
        else:
            return "print_odd_day"

    # Define a task to print a message for even days
    @task
    def print_even_day() -> None:
        print("This is an even day.")

    # Define a task to print a message for odd days
    @task
    def print_odd_day() -> None:
        print("This is an odd day.")

    # Define the end task using the EmptyOperator with a specific trigger rule
    end = EmptyOperator(
        task_id="end", trigger_rule="none_failed_min_one_success"
    )

    # Set the branching logic
    branch = choose_branch()
    # Define the task dependencies
    start >> branch  # Start task triggers the branching task

    # Branching task triggers the even day task, which then triggers the end task
    branch >> print_even_day() >> end

    # Branching task triggers the odd day task, which then triggers the end task
    branch >> print_odd_day() >> end


# Instantiate the DAG
demo_branching()
