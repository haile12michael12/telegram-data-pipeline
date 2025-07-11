-- models/marts/dim_channels.sql

select distinct
  channel_name
from {{ ref('stg_telegram_messages') }}
