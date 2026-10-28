from __future__ import annotations

import pandas as pd
from google.cloud import bigquery

from src.config import settings


def load_category_demand(category: str | None = None) -> pd.DataFrame:
    """Load one category's daily demand from the dbt mart in BigQuery."""
    category = category or settings.forecast_category
    client = bigquery.Client(project=settings.gcp_project_id, location=settings.bq_location)
    table = f"{settings.gcp_project_id}.{settings.bq_dataset}.mart_daily_category_demand"

    query = f"""
        SELECT
            order_date,
            product_category,
            units_sold,
            orders,
            gross_revenue,
            average_selling_price
        FROM `{table}`
        WHERE product_category = @category
        ORDER BY order_date
    """
    config = bigquery.QueryJobConfig(
        query_parameters=[bigquery.ScalarQueryParameter("category", "STRING", category)]
    )
    df = client.query(query, job_config=config).to_dataframe()
    if df.empty:
        raise ValueError(f"No demand data found for category: {category}")
    return df
