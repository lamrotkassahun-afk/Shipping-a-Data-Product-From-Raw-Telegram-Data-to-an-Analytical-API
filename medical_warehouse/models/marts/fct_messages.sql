{{ config(materialized='table') }}

SELECT
    message_id,
    MD5(channel_name) AS channel_key,
    message_date,
    message_text,
    views AS view_count,
    forwards AS forward_count
FROM {{ ref('stg_telegram_messages') }}