import pendulum
from airflow import DAG
from airflow.providers.standard.operators.python import PythonOperator


# Define the Python functions that will be used as tasks in the DAG.
def print_hello() -> None:
    print("Hello from task 1")
    raise Exception("This is an exception")


def print_goodbye() -> None:
    print("Goodbye from task 2")


# Define default arguments for the DAG.
default_args = {
    "owner": "airflow",  # Owner of the DAG.
    "start_date": pendulum.today("UTC").add(days=-1),  # Start date of the DAG.
}

# Define the DAG using a context manager.
with DAG(
    "demo_triggers",  # Name of the DAG.
    default_args=default_args,  # Default arguments for the DAG.
    schedule="@daily",  # Schedule interval for the DAG.
) as dag:
    # Define the first task using PythonOperator.
    task1 = PythonOperator(
        task_id="task1",  # Unique ID for the task.
        python_callable=print_hello,  # Python function to be called.
    )

    # Define the second task using PythonOperator.
    task2 = PythonOperator(
        task_id="task2",  # Unique ID for the task.
        python_callable=print_goodbye,  # Python function to be called.
        # The trigger_rule parameter determines when this task should be executed.
        # 'none_failed_min_one_success' means that this task will be triggered
        # trigger_rule="all_success",
        # 'all_done' means that this task will be triggered regardless of the
        # status of upstream tasks.
        trigger_rule="all_done",
        # 'one_failed' means that this task will be triggered if any upstream
        # task has failed.
        # trigger_rule="one_failed",
        # 'none_failed' means that this task will be triggered only if no
        # upstream tasks have failed.
        # trigger_rule="none_failed",
        # 'none_skipped' means that this task will be triggered only if no
        # upstream tasks have been skipped.
        # trigger_rule="none_skipped",
        # 'always' means that this task will be triggered regardless of the
        # status of upstream tasks.
        # Difference between 'all_done' and 'always' is that 'all_done' will
        # not trigger this task if upstream tasks have been skipped.
        # trigger_rule="always",
        # 'none_failed_min_one_success' means that this task will be triggered
        # if at least one upstream task has succeeded and no upstream tasks
        # have failed.
        # trigger_rule="none_failed_min_one_success",
    )

    # This sets up the dependency such that task2 will be executed after
    # task1.
    task1 >> task2
