# PostgreSQL Docker Environment Setup

## Run the Docker Compose file to set up the environment

To run the Docker Compose file, you need to have Docker and Docker Compose installed on your machine. Once you have them installed, follow these steps:
1. Open a terminal or command prompt.
1. Change to the directory where the `docker-compose.yml` file is located.
1. Run the following command to start the services defined in the `docker-compose.yml` file:
    ```bash
    docker-compose up -d
    ```
1. This command will start the services in detached mode, allowing them to run in the background.
1. You can check the status of the services by running:
    ```bash
    docker-compose ps
    ```
1. To stop the services, you can run:
    ```bash
    docker-compose down
    ```
    This will stop and remove the containers defined in the `docker-compose.yml` file.
1. Make sure to check the logs for any errors or issues during the startup process. You can view the logs of a specific service by running:
    ```bash
    docker-compose logs <service_name>
    ```
    Replace `<service_name>` with the name of the service you want to check.
    If you encounter any issues, refer to the Docker documentation or the specific service documentation for troubleshooting steps.

## Accessing the PostgreSQL Database

### PgAdmin Access

PgAdmin: http://localhost:8090/
User: dbuser@dbhost.data
Password: dbpass

Register the database server in PgAdmin with the following details:

Host: database
Port: 5432
Username: postgres
Password: `<NO PASSWORD>`
Database: postgres

Once registered, you can manage your PostgreSQL database through the PgAdmin interface.

### PostgreSQL Database Connection From Host

To access the PostgreSQL database from your host machine, you can use any PostgreSQL client (like `psql`, DBeaver, or PgAdmin) with the following connection details:

Host: 127.0.0.1
Port: 5090
Username: postgres
Password: `<NO PASSWORD>`
Database: postgres

SQL Alchemy Connection String: `postgresql+psycopg2://airflow_user:airflow_pass@127.0.0.1:5090/airflow_db`

