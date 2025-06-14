import pendulum
from airflow import DAG
from airflow.decorators import task

# Default arguments for the DAG, including the owner and start date
default_args = {
    "owner": "airflow",
    "start_date": pendulum.today("UTC").add(
        days=-1
    ),  # Start date is set to yesterday
}

# Define the DAG with a daily schedule
with DAG(
    "demo_triggers",  # Name of the DAG
    default_args=default_args,  # Default arguments defined above
    schedule="@daily",  # Schedule interval for the DAG
) as dag:
    # Define the first task using the task decorator
    @task
    def print_hello() -> None:
        # This task prints a hello message
        print("Hello from task 1")

    # Define the second task with a specific trigger rule
    @task(trigger_rule="none_failed_min_one_success")
    def print_goodbye() -> None:
        # This task prints a goodbye message
        print("Goodbye from task 2")

    # Instantiate the tasks
    hello_task = print_hello()
    goodbye_task = print_goodbye()

    # Set the task dependencies
    # hello_task must run successfully before goodbye_task can run
    hello_task >> goodbye_task
