import logging
import os
from typing import Any, Dict, List

import pendulum
from airflow import DAG
from airflow.providers.standard.operators.empty import EmptyOperator
from airflow.providers.standard.operators.python import PythonOperator
from airflow.providers.standard.sensors.filesystem import FileSensor
from airflow.utils.task_group import TaskGroup

logger = logging.getLogger(__name__)


# Reads stock symbols from a file and returns them as a list of strings.
def read_stock_symbols(stocks_file: str, **context: Any) -> List[str]:
    try:
        with open(stocks_file, "r") as file:
            return [line.strip() for line in file.readlines()]
    except Exception as e:
        logger.error(
            f"Failed to read stock symbols from {stocks_file}: {e}",
            exc_info=True,
        )
        raise


# Looks up stock prices for the given symbols and writes them to a file.
def lookup_stock_prices(prices_file: str, **context: Any) -> None:
    import yfinance as yf  # type: ignore

    ti = context["ti"]
    try:
        symbols: List[str] = ti.xcom_pull(task_ids="read_stock_symbols")
        prices: Dict[str, Any] = {}
        for symbol in symbols:
            try:
                stock = yf.Ticker(symbol)
                prices[symbol] = stock.history(period="1d")["Close"][0]
            except Exception as e:
                logger.error(
                    f"Failed to fetch price for {symbol}: {e}", exc_info=True
                )
                prices[symbol] = None
        with open(prices_file, "w") as file:
            for symbol, price in prices.items():
                file.write(f"{symbol}: {price}\n")
    except Exception as e:
        logger.error(f"Failed to lookup stock prices: {e}", exc_info=True)
        raise


# Looks up stock volumes for the given symbols and writes them to a file.
def lookup_stock_volumes(volumes_file: str, **context: Any) -> None:
    import yfinance as yf  # type: ignore

    ti = context["ti"]
    try:
        symbols: List[str] = ti.xcom_pull(task_ids="read_stock_symbols")
        volumes: Dict[str, Any] = {}
        for symbol in symbols:
            try:
                stock = yf.Ticker(symbol)
                volumes[symbol] = stock.history(period="1d")["Volume"].iloc[0]
            except Exception as e:
                logger.error(
                    f"Failed to fetch volume for {symbol}: {e}", exc_info=True
                )
                volumes[symbol] = None
        with open(volumes_file, "w") as file:
            for symbol, volume in volumes.items():
                file.write(f"{symbol}: {volume}\n")
    except Exception as e:
        logger.error(f"Failed to lookup stock volumes: {e}", exc_info=True)
        raise


# Deletes the stocks file after processing.
def delete_stocks_file(stocks_file: str, **context: Any) -> None:
    try:
        os.remove(stocks_file)
    except Exception as e:
        logger.error(
            f"Failed to delete stocks file {stocks_file}: {e}", exc_info=True
        )
        raise


# Define the DAG (Directed Acyclic Graph) for Airflow
with DAG(
    dag_id="lookup_stocks",
    schedule=None,
    start_date=pendulum.datetime(2025, 1, 1, tz="UTC"),
    catchup=False,
    params={
        "stocks_file": "/tmp/stocks.txt",
        "prices_file": "/tmp/stock_prices.txt",
        "volumes_file": "/tmp/stock_volumes.txt",
    },
) as dag:
    # Dummy start task
    start = EmptyOperator(task_id="start")

    # Wait for the stocks file to appear in the filesystem
    wait_for_file = FileSensor(
        task_id="wait_for_stocks_file",
        filepath="{{ params.stocks_file }}",
        poke_interval=10,
        timeout=600,
    )

    # Task to read stock symbols from file
    read_symbols = PythonOperator(
        task_id="read_stock_symbols",
        python_callable=read_stock_symbols,
        op_args=["{{ params.stocks_file }}"],
    )

    # Group for lookup tasks (prices and volumes)
    with TaskGroup(group_id="lookup_tasks") as lookup_tasks:
        # Task to look up stock prices
        lookup_prices = PythonOperator(
            task_id="lookup_stock_prices",
            python_callable=lookup_stock_prices,
            op_args=["{{ params.prices_file }}"],
        )

        # Task to look up stock volumes
        lookup_volumes = PythonOperator(
            task_id="lookup_stock_volumes",
            python_callable=lookup_stock_volumes,
            op_args=["{{ params.volumes_file }}"],
        )

    # Task to delete the stocks file after processing
    end = PythonOperator(
        task_id="end",
        python_callable=delete_stocks_file,
        op_args=["{{ params.stocks_file }}"],
    )

    # Define task dependencies: start -> wait_for_file -> read_symbols -> lookup_tasks -> end
    start >> wait_for_file >> read_symbols >> lookup_tasks >> end
