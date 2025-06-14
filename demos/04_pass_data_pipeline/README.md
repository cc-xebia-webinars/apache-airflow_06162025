# Pass Data Pipeline

## Instructions

1. Review the `demo_pass_data.py` file.

1. Copy `demo_pass_data` DAG to the Airflow `dags` folder.

    ```bash
    cp demo_pass_data.py ~/airflow/dags/
    ```

1. List the tasks for the `demo_pass_data` DAG.

    ```bash
    airflow tasks list demo_pass_data
    ```

    There should be two tasks listed: `get_greeting` and `print_greeting`.

1. Trigger the `demo_pass_data` DAG

    ```bash
    airflow dags test demo_pass_data
    ```

    Review the output for the "Hello, world!" greeting. It can be hard to find, just look closely and carefully.
