{{ config(materialized='table') }}

WITH yolo_data AS (
    SELECT
        message_id,
        image_category,
        confidence_score
    FROM {{ ref('yolo_detections') }}
),

message_data AS (
    SELECT
        message_id,
        channel_name,
        view_count
    FROM {{ ref('stg_telegram_messages') }} -- Reference staging here
)

SELECT
    m.message_id,
    m.channel_name,
    y.image_category,
    y.confidence_score,
    m.view_count
FROM yolo_data y
JOIN message_data m ON y.message_id = m.message_id