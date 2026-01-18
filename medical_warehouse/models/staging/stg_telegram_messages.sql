{{ config(materialized='view') }}

SELECT
    message_id,
    channel_name,
    channel_title,  -- Ensure this matches the raw table column name
    CAST(message_date AS TIMESTAMP) AS message_date,
    message_text,
    views,           -- Use 'views' here so the Marts can alias it
    forwards,        -- Use 'forwards' here
    image_path
FROM {{ source('raw', 'telegram_messages') }}
WHERE message_id IS NOT NULL