from datetime import timedelta

from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.utils.dates import days_ago


default_args = {
    "owner": "newsbot",
    "depends_on_past": False,
    "retries": 1,
    "retry_delay": timedelta(minutes=5),
}

with DAG(
    dag_id="newsbot_daily_workflow",
    default_args=default_args,
    description="Scrape VnExpress, summarize latest articles and send Telegram updates.",
    schedule_interval="0 0 * * *",
    start_date=days_ago(1),
    catchup=False,
    max_active_runs=1,
    tags=["newsbot"],
) as dag:
    scrape = BashOperator(
        task_id="scrape_vnexpress",
        bash_command="cd /opt/airflow/app && python run_scrape.py",
    )

    summarize = BashOperator(
        task_id="summarize_latest_articles",
        bash_command="cd /opt/airflow/app && python run_summary.py",
    )

    scrape >> summarize
