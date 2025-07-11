-- models/marts/fct_messages.sql

select
  message_id,
  channel_name,
  date::date as date_id,
  sender_id,
  message_length,
  has_image
from {{ ref('stg_telegram_messages') }}
