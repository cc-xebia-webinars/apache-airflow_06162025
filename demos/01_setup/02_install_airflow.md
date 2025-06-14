# Install Airflow

## Part 1 - Install Airflow

1. Open a terminal window in VS Code by clicking on the `Terminal` menu and
selecting `New Terminal`. You may use the regular system terminal if you
prefer. Type the following command, and press `Enter`.

    ```sh
    export AIRFLOW_HOME=~/airflow
    ```

    This command sets the `AIRFLOW_HOME` environment variable to direct Airflow
    to use the `~/airflow` folder as the home directory. When Airflow is
    installed, it will use this folder to store configuration files, logs, and
    other data.

    If you are new to Linux, the `~` character is a shortcut for your home
    directory. The `~/airflow` path is the same as
    `/home/yourusername/airflow`.

1. In the `01_setup` folder of the course repository, with VS Code, create a
new file named `install_airflow.sh`. Copy the following code to the file.

    ```sh
    AIRFLOW_VERSION=3.0.2

    # Extract the version of Python you have installed. If you're currently using a Python version that is not supported by Airflow, you may want to set this manually.
    # See above for supported versions.
    PYTHON_VERSION="$(python -c 'import sys; print(f"{sys.version_info.major}.{sys.version_info.minor}")')"

    CONSTRAINT_URL="https://raw.githubusercontent.com/apache/airflow/constraints-${AIRFLOW_VERSION}/constraints-${PYTHON_VERSION}.txt"
    # For example this would install 3.0.0 with python 3.9: https://raw.githubusercontent.com/apache/airflow/constraints-3.0.2/constraints-3.9.txt

    pip install "apache-airflow==${AIRFLOW_VERSION}" --constraint "${CONSTRAINT_URL}"
    ```

1. In the terminal, change to the `demos/01_setup` folder of the course
repository. If you are unsure how to do this, please ask for assistance.

1. Make the `install_airflow.sh` file executable.

    ```sh
    chmod +x install_airflow.sh
    ```

1. Run the `install_airflow.sh` script.

    ```sh
    ./install_airflow.sh
    ```

    The script will install Airflow version `2.10.4` and the necessary
    dependencies.


## Part 2 - Run Airflow

1. Open a new terminal window if you do not already have a terminal window
open. Type the following command and press `Enter`.

    ```sh
    airflow standalone
    ```

    This command will start the Airflow web server and scheduler. The web
    server will be available at `http://localhost:8080`. The scheduler will
    start running tasks as they are scheduled.

    As part of the console output, you will see a message that the web server
    is running. You can press `Ctrl+C` to stop the web server and scheduler.

    The admin username and password will be displayed in the console output.

1. Open a web browser and navigate to `http://localhost:8080`. You will see the
Airflow web interface. Log in using the admin username and password displayed
in the console output.

1. Review the Airflow web interface.

1. After starting Airflow with `airflow standalone`, review the `AIRFLOW_HOME` folder to see
    the files and folders created by Airflow.

    ```sh
    ls ~/airflow
    ```

1. To view the Airflow web server process id, type the following command and press `Enter`.

    ```sh
    cat ~/airflow/airflow-webserver.pid
    ```

    This command will display the process id of the Airflow web server. You can
    use this process id to stop the web server if needed.

    ```sh
    kill -9 <process_id>
    ```

1. Also, to stop the Airflow web server from the terminal where it launched, press `Ctrl+C`.

1. The Airflow `admin` standalone password can be located here:

    ```sh
    cat ~/airflow/simple_auth_manager_passwords.json.generated
    ```

    This command will display the password for the `admin` user. You can use
    this password to log in to the Airflow web interface.

1. Stop the Airflow standalone process by pressing `Ctrl+C` in the terminal where it is running.

1. Let's make three modifications to the Airflow configuration file. Edit the `$AIRFLOW_HOME/airflow.cfg` file and make the following changes.

    Find the `AIRFLOW__CORE__LOAD_EXAMPLES` setting and change the value to the following.`

    ```text
    load_examples = False
    ```

    Find the `AIRFLOW__LOGGING__LOGGING_LEVEL` setting and change the value to the following.

    ```text
    logging_level = ERROR
    ```

    Find the `AIRFLOW__DAG_PROCESSOR__REFRESH_INTERVAL` setting and change the value to the following.

    ```text
    refresh_interval = 20
    ```

1. Start the Airflow web server and scheduler again.

    ```sh
    airflow standalone
    ```

1. Open a web browser and navigate to `http://localhost:8080`. You will see the
Airflow web interface. Log in using the admin username and password displayed
in the console output.

1. Review the Airflow web interface. You should see no DAGs listed.