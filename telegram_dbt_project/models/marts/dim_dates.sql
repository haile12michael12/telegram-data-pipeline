-- models/marts/dim_dates.sql

select distinct
  date::date as date_id,
  extract(day from date) as day,
  extract(month from date) as month,
  extract(year from date) as year
from {{ ref('stg_telegram_messages') }}
