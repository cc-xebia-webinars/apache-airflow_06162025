# Hello World Pipeline

## Demo Instructions

1. Review the `demo_hello_world.py` file.

1. List DAGs with the name `demo_hello_world`.

    ```bash
    airflow dags list | grep demo_hello_world
    ```

    There should no DAGs listed.

1. Copy `demo_hello_world` DAG to the Airflow `dags` folder.

    ```bash
    cp demo_hello_world.py ~/airflow/dags/
    ```

1. List DAGs with the name `demo_hello_world`.

    ```bash
    airflow dags list | grep demo_hello_world
    ```

    There should be one DAG listed. When copying over DAGs, it is not needed to restart Airflow.

1. List the tasks for the `demo_hello_world` DAG.

    ```bash
    airflow tasks list demo_hello_world
    ```

    There should be one task listed.

1. Trigger the `demo_hello_world` task.

    ```bash
    airflow tasks test demo_hello_world hello_world
    ```

    Review the output for the message "Hello World". It can be hard to find, just look closely and carefully.

1. Trigger the `demo_hello_world` DAG

    ```bash
    airflow dags test demo_hello_world
    ```

    Review the output for the message "Hello World". It can be hard to find, just look closely and carefully.

1. Repeat the above steps with the `demo_with_hello_world` DAG.


