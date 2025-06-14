# Multiple Tasks Pipeline

## Instructions

1. Review the `demo_multiple_tasks.py` file.

1. Copy `demo_multiple_tasks` DAG to the Airflow `dags` folder.

    ```bash
    cp demo_multiple_tasks.py ~/airflow/dags/
    ```

1. List the tasks for the `demo_multiple_tasks` DAG.

    ```bash
    airflow tasks list demo_multiple_tasks
    ```

    There should be two tasks listed: `hello_world` and `goodbye_world`.

1. Trigger the `hello_world` task.

    ```bash
    airflow tasks test demo_multiple_tasks hello_world
    ```

    Review the output for the message "Hello, world!". It can be hard to find, just look closely and carefully.

1. Trigger the `goodbye_world` task.

    ```bash
    airflow tasks test demo_multiple_tasks goodbye_world
    ```

    Review the output for the message "Goodbye, world!". It can be hard to find, just look closely and carefully.

1. Trigger the `demo_multiple_tasks` DAG

    ```bash
    airflow dags test demo_multiple_tasks
    ```

    Review the output for the messages, "Hello, world!" and "Goodbye, world!". It can be hard to find, just look closely and carefully.

