import os
from typing import List, cast

import pendulum
from airflow.decorators import dag, task
from airflow.models.param import Param
from airflow.providers.standard.operators.empty import EmptyOperator
from airflow.providers.standard.sensors.filesystem import FileSensor


# Define the DAG using the TaskFlow API
@dag(
    dag_id="lookup_stocks_task_flow",
    schedule=None,  # No schedule, manual trigger
    start_date=pendulum.datetime(2023, 3, 3, tz="UTC"),
    catchup=False,
    params={
        "stocks_file": Param("/tmp/stocks.txt", type="string"),
        "stock_prices_file": Param("/tmp/stock_prices.txt", type="string"),
        "stock_volumes_file": Param("/tmp/stock_volumes.txt", type="string"),
    },
)
def lookup_stocks_task_flow() -> None:
    # Dummy start task
    start = EmptyOperator(task_id="start")

    # Wait for the stocks file to appear in the filesystem
    wait_for_file = FileSensor(
        task_id="wait_for_stocks_file",
        filepath="{{ params.stocks_file }}",
        poke_interval=10,
        timeout=600,
    )

    # Task to read stock symbols from a file
    @task
    def read_stock_symbols(stocks_file: str) -> List[str]:
        with open(stocks_file, "r") as file:
            return [line.strip() for line in file.readlines()]

    # Task to look up stock prices using yfinance and write to a file
    @task
    def lookup_stock_prices(
        symbols: List[str], stock_prices_file: str
    ) -> None:
        import yfinance as yf  # type: ignore

        prices = {}
        for symbol in symbols:
            stock = yf.Ticker(symbol)
            prices[symbol] = stock.history(period="1d")["Close"][0]
        with open(stock_prices_file, "w") as file:
            for symbol, price in prices.items():
                file.write(f"{symbol}: {price}\n")

    # Task to look up stock volumes using yfinance and write to a file
    @task
    def lookup_stock_volumes(
        symbols: List[str], stock_volumes_file: str
    ) -> None:
        import yfinance as yf  # type: ignore

        volumes = {}
        for symbol in symbols:
            stock = yf.Ticker(symbol)
            volumes[symbol] = stock.history(period="1d")["Volume"][0]
        with open(stock_volumes_file, "w") as file:
            for symbol, volume in volumes.items():
                file.write(f"{symbol}: {volume}\n")

    # Task to delete the stocks file after processing
    @task
    def delete_stocks_file(stocks_file: str) -> None:
        os.remove(stocks_file)

    # Read stock symbols from file
    symbols = read_stock_symbols("{{ params.stocks_file }}")
    # Look up prices and volumes for the symbols
    prices = lookup_stock_prices(
        cast(list[str], symbols), "{{ params.stock_prices_file }}"
    )
    volumes = lookup_stock_volumes(
        cast(list[str], symbols), "{{ params.stock_volumes_file }}"
    )

    # Define task dependencies
    start >> wait_for_file >> symbols
    [prices, volumes] >> delete_stocks_file("{{ params.stocks_file }}")


# Instantiate the DAG
lookup_stocks_task_flow()
