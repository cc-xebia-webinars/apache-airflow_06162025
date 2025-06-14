# Airflow PostgreSQL

1. Ensure the PostgreSQL container is running.

1. From the `12_postgresql` demo folder, execute the SQL script `create_airflow_db.sql` file with Docker using the `psql` command.

    ```bash
    cat ./create_airflow_db.sql | docker exec -i b357 psql -h localhost -p 5432 -U postgres -d postgres
    ```

1. Install the `psycopg2` package.

    ```bash
    python -m pip install psycopg2-binary asyncpg
    ```

1. Modify the `$AIRFLOW_HOME/airflow.cfg` file to use the new PostgreSQL database. Open the `airflow.cfg` file in your editor and find the `AIRFLOW__DATABASE__SQL_ALCHEMY_CONN` setting. Change the value to the following.

    ```text
    postgresql+psycopg2://airflow_user:airflow_pass@127.0.0.1:5090/airflow_db
    ```

    In class, we may use the `postgres` user if there are permission issues with the `airflow_user` user.

    ```text
    postgresql+psycopg2://postgres@127.0.0.1:5090/airflow_db
    ```

1. Migrate the database to the PostgreSQL database.

    ```bash
    airflow db migrate
    ```

## Run Airflow

1. Start the Airflow webserver.

    ```bash
    airflow api-server --port 8080 -D
    ```

1. Start the Airflow scheduler.

    ```bash
    airflow scheduler -D
    ```

1. Start the Airflow DAG processor.

    ```bash
    airflow dag-processor -D
    ```

1. Start the Airflow triggerer.

    ```bash
    airflow triggerer -D
    ```

1. Open a web browser and go to `http://localhost:8080`. Log in with the admin user you created.

1. The DAG we are going to test needs the `FileSensor`. When Airflow was configured with PostgreSQL, none of the default connections were created. We need to create a connection for the `FileSensor` to use. Click on the **Admin** menu and select **Connections**. Click on the **+** button to create a new connection. Enter the following values.

    - Conn Id: `fs_default`
    - Conn Type: `fs`

    Click on the **Save** button to save the new connection.

1. Ensure the `$AIRFLOW_HOME/dags` folder exists.

    ```bash
    mkdir -p $AIRFLOW_HOME/dags
    ```

1. Copy the `lookup_stocks.py` file to the `dags` folder.

    ```bash
    cp lookup_stocks.py $AIRFLOW_HOME/dags
    ```

1. Verify the `lookup_stocks` DAG is in the list of DAGs in the Airflow web UI. Unpause the DAG.

1. Copy the `stocks.txt` file to the `/tmp` folder.

    ```bash
    cp stocks.txt /tmp
    ```

1. Review the execution of the `lookup_stocks` DAG in the Airflow web UI. It should run successfully.

1. Verify the `stock_prices.txt` and `stock_volumes.txt` files were created in the `/tmp` folder.