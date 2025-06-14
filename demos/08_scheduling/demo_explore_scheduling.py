from datetime import datetime

from airflow import DAG
from airflow.providers.standard.operators.python import PythonOperator


def print_message():
    print(f">>>>> Explore Scheduling Demo: {datetime.now()} <<<<<<".upper())


# The `schedule_interval` parameter in Airflow uses a cron expression to define the frequency at which the DAG (Directed Acyclic Graph) should run. The cron expression consists of five fields separated by spaces, each representing a unit of time. The fields are as follows:

# 1. **Minute** (0-59)
# 2. **Hour** (0-23)
# 3. **Day of the month** (1-31)
# 4. **Month** (1-12)
# 5. **Day of the week** (0-6, where 0 is Sunday)

# The expression `"* * * * *"` means that the DAG will run every minute. Here's a breakdown of the expression:

# - `*` in the minute field means every minute.
# - `*` in the hour field means every hour.
# - `*` in the day of the month field means every day of the month.
# - `*` in the month field means every month.
# - `*` in the day of the week field means every day of the week.

# So, `"* * * * *"` translates to "run every minute of every hour of every day of every month."

# Here are some common cron expression shortcuts that can be used in the `schedule_interval` parameter in Airflow:

# 1. **@once**: Run the DAG once and only once.
# 2. **@hourly**: Run the DAG every hour.
# 3. **@daily**: Run the DAG once a day at midnight.
# 4. **@weekly**: Run the DAG once a week at midnight on Sunday.
# 5. **@monthly**: Run the DAG once a month at midnight on the first day of the month.
# 6. **@yearly** or **@annually**: Run the DAG once a year at midnight on January 1st.

# These shortcuts can simplify the cron expressions and make the schedule intervals more readable. For example:

with DAG(
    "demo_explore_scheduling",
    default_args={
        "start_date": datetime(2025, 1, 1),
    },
    # No schedule
    # schedule=None,
    # Schedule interval to run every 10 seconds
    # schedule="*/10 * * * * *",
    # Schedule interval to run every 30 seconds
    schedule="*/30 * * * * *",
    # Schedule interval to run every 1 minute
    # schedule="* * * * *",
    # Schedule interval to run every 5 minutes
    # schedule="*/5 * * * *",
    # Schedule interval to run every 10 minutes
    # schedule="*/10 * * * *",
    # Schedule interval to run every 30 minutes
    # schedule="*/30 * * * *",
    # Schedule interval to run every hour
    # schedule="0 * * * *",
    # Schedule interval to run every 2 hours
    # schedule="0 */2 * * *",
    # Schedule interval to run every 3 hours
    # schedule="0 */3 * * *",
    # Schedule interval to run every 6 hours
    # schedule="0 */6 * * *",
    # Schedule interval to run every 12 hours
    # schedule="0 */12 * * *",
    # Schedule interval to run daily at midnight
    # schedule="0 0 * * *",
    # Schedule interval to run daily at 6 AM
    # schedule="0 6 * * *",
    # Schedule interval to run daily at 6 PM
    # schedule="0 18 * * *",
    # Schedule interval to run weekly on Sunday at midnight
    # schedule="0 0 * * 0",
    # Schedule interval to run weekly on Monday at midnight
    # schedule="0 0 * * 1",
    # Schedule interval to run weekly on Friday at midnight
    # schedule="0 0 * * 5",
    # Schedule interval to run monthly on the first day at midnight
    # schedule="0 0 1 * *",
    # Schedule interval to run monthly on the last day at midnight
    # schedule="0 0 L * *",
    # Schedule interval to run yearly on January 1st at midnight
    # schedule="0 0 1 1 *",
    # Schedule interval to run every 2 years on January 1st at midnight
    # schedule="0 0 1 1 */2",
) as dag:
    print_message_task = PythonOperator(
        task_id="print_message",
        python_callable=print_message,
    )

    print_message_task
