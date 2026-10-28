from __future__ import annotations

from datetime import datetime

from airflow import DAG
from airflow.operators.bash import BashOperator


with DAG(
    dag_id="retail_demand_forecasting",
    description="Build dbt marts, train demand model, and run tests.",
    start_date=datetime(2026, 1, 1),
    schedule="0 5 * * *",
    catchup=False,
    tags=["retail", "forecasting", "dbt", "ml"],
) as dag:
    dbt_build = BashOperator(
        task_id="dbt_build",
        bash_command="cd /opt/airflow/project/dbt && dbt build --profiles-dir .",
    )

    train_model = BashOperator(
        task_id="train_model",
        bash_command="cd /opt/airflow/project && python -m src.train",
    )

    unit_tests = BashOperator(
        task_id="unit_tests",
        bash_command="cd /opt/airflow/project && pytest -q",
    )

    dbt_build >> train_model >> unit_tests
