-- models/tests/test_no_null_length_for_images.sql

select *
from {{ ref('fct_messages') }}
where has_image = true and message_length is null
