-- Example operational monitoring query for the daily demand mart.
-- Intended to be run after dbt build or adapted into a scheduled BigQuery check.

WITH recent AS (
  SELECT
    order_date,
    product_category,
    units_sold,
    gross_revenue
  FROM `${GCP_PROJECT_ID}.${BQ_DATASET}.mart_daily_category_demand`
  WHERE order_date >= DATE_SUB(CURRENT_DATE(), INTERVAL 14 DAY)
)
SELECT
  COUNTIF(product_category IS NULL) AS null_categories,
  COUNTIF(units_sold < 0) AS negative_unit_rows,
  COUNTIF(gross_revenue < 0) AS negative_revenue_rows,
  COUNT(*) AS rows_checked,
  MAX(order_date) AS latest_business_date
FROM recent;
