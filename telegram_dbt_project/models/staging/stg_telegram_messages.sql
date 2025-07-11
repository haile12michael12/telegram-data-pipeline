-- models/staging/stg_telegram_messages.sql

with source as (
  select * from raw.telegram_messages
),

cleaned as (
  select
    id as message_id,
    channel_name,
    message,
    date,
    sender_id,
    length(message) as message_length,
    raw_json->'media' is not null as has_image
  from source
)

select * from cleaned
