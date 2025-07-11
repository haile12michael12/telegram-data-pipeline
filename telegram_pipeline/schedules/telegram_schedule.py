# telegram_pipeline/schedules/telegram_schedule.py

from dagster import ScheduleDefinition
from ..jobs.telegram_job import telegram_data_pipeline

telegram_daily_schedule = ScheduleDefinition(
    job=telegram_data_pipeline,
    cron_schedule="0 6 * * *",  # every day at 6 AM
    execution_timezone="UTC",
    name="daily_telegram_schedule"
)
