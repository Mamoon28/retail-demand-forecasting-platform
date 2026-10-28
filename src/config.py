from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    gcp_project_id: str = "your-gcp-project-id"
    bq_dataset: str = "retail_demand"
    bq_location: str = "US"
    forecast_category: str = "Outerwear & Coats"
    lookback_days: int = 28
    forecast_horizon: int = 7
    model_artifact_dir: Path = Path("artifacts")

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")


settings = Settings()
