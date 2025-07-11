# Calls scraper, loader, yolo, dbt

# telegram_pipeline/ops/telegram_ops.py

from dagster import op
import subprocess

@op
def scrape_telegram_data():
    subprocess.run(["python", "src/ingestion/telegram_scraper.py"], check=True)

@op
def load_raw_to_postgres():
    subprocess.run(["python", "src/transformation/load_raw_json.py"], check=True)

@op
def run_dbt_transformations():
    subprocess.run(["dbt", "run", "--project-dir", "telegram_dbt_project"], check=True)

@op
def run_yolo_enrichment():
    subprocess.run(["python", "src/enrichment/yolo_detector.py"], check=True)
    subprocess.run(["python", "src/transformation/load_image_detections.py"], check=True)
