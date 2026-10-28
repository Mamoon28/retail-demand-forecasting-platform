# Interview Notes — How to Explain the Project

## 30-second version
I built an end-to-end retail demand forecasting platform using Google's public theLook e-commerce data in BigQuery. I used dbt to create tested staging, fact, dimension, and demand-mart models; trained and compared seasonal-naive, ARIMA, and TensorFlow/Keras LSTM forecasts; exposed the trained model through FastAPI; containerised it with Docker; and added automated unit tests and GitHub Actions CI. I also included an Airflow DAG to demonstrate how the data and model workflow could be orchestrated.

## Why this design?
- **BigQuery**: cloud warehouse and direct access to a public e-commerce dataset.
- **dbt**: separates raw-source logic, reusable transformations, tests, and analytics marts.
- **Star-style model**: makes downstream analytics easier to reason about and reuse.
- **Seasonal naive baseline**: a complex model should beat a simple weekly pattern before being considered useful.
- **ARIMA**: classical statistical baseline and a bridge from prior forecasting experience.
- **LSTM**: demonstrates deep-learning forecasting while keeping the architecture explainable.
- **FastAPI**: shows how a trained model can become a software-facing service rather than remain in a notebook.
- **Docker**: reproducible runtime for model serving.
- **GitHub Actions**: validates code quality and unit tests on changes.
- **Airflow DAG**: demonstrates orchestration of data transformation, model training, and tests.

## Important honesty line
This is a portfolio system, not an Ocado-scale production platform. I built it to practise the same engineering patterns: tested transformations, reproducible training, model serving, orchestration, CI, and clear separation of responsibilities.

## Questions to expect
### Why not random train/test split?
Time series must preserve chronology. A random split would leak future information into training and produce an unrealistically optimistic result.

### Why compare against a naive model?
Forecasting models should create incremental value. If an LSTM cannot outperform a simple weekly seasonal baseline, its operational complexity is hard to justify.

### What would you monitor in production?
Input data freshness and schema changes, missing values, feature drift, prediction distribution, forecast error by category and horizon, service latency/error rate, and retraining performance.

### How would you improve this?
Add multi-series/global forecasting across categories, richer product/inventory features, promotion and calendar features, probabilistic forecasts, transformer architectures, model registry/versioning, scheduled retraining, and production observability.

### How does it relate to Ocado?
The exact retail problem is simplified, but the lifecycle is relevant to logistics/supply-chain ML: warehouse transformations, demand features, forecasting, model evaluation, service integration, testing, orchestration, and monitoring.
