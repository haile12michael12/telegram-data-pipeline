-- models/marts/fct_image_detections.sql

select
  det.message_id,
  msg.channel_name,
  det.detected_object_class,
  det.confidence_score
from {{ ref('stg_image_detections') }} det
left join {{ ref('fct_messages') }} msg
  on det.message_id = msg.message_id
