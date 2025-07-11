-- models/staging/stg_image_detections.sql

select
  message_id,
  channel_name,
  detected_object_class,
  confidence_score
from raw.image_detections
