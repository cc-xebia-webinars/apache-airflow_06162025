# Catch up

1. Review the `demo_explore_catchup.py` file.

1. Copy `demo_catchup` DAG to the Airflow `dags` folder.

   ```bash
   cp demo_explore_catchup.py ~/airflow/dags/
   ```

1. Open the web browser, navigate to the list of DAGs, and click `Refresh`. You may need to click it a few times.

1. Activate the `demo_explore_catchup` DAG.

1. Review the event logs, the DAGs will execute for each day leading up to today. It is catching up!

