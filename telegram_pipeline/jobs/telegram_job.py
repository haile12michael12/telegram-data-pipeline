# Defines pipeline job
# telegram_pipeline/jobs/telegram_job.py

from dagster import job
from ..ops.telegram_ops import (
    scrape_telegram_data,
    load_raw_to_postgres,
    run_dbt_transformations,
    run_yolo_enrichment
)

@job
def telegram_data_pipeline():
    scrape_telegram_data()
    load_raw_to_postgres()
    run_yolo_enrichment()
    run_dbt_transformations()
