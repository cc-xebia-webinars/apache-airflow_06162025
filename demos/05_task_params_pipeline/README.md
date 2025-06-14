# Task Params Pipeline

## Instructions

1. Review the `task_params.py` file.

1. Copy `task_params` DAG to the Airflow `dags` folder.

    ```bash
    cp task_params.py ~/airflow/dags/
    ```

1. List the tasks for the `task_params` DAG.

    ```bash
    airflow tasks list task_params
    ```

    There should be two tasks listed: `get_greeting` and `print_greeting`.

1. Trigger the `task_params` DAG

    ```bash
    airflow dags test task_params
    ```

    Review the output for the "Hello, John!" greeting. It can be hard to find, just look closely and carefully.

