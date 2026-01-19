{{ config(materialized='view') }}

SELECT
    message_id,
    channel_name,
    channel_title,
    CAST(message_date AS TIMESTAMP) AS message_date,
    message_text,
    views AS view_count,    -- Add 'AS view_count' to fix the error
    forwards AS forward_count, -- Add 'AS forward_count' for consistency
    image_path
FROM {{ source('raw', 'telegram_messages') }}
WHERE message_id IS NOT NULL