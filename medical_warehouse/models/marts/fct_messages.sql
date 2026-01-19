{{ config(materialized='table') }}

SELECT
    message_id,
    channel_name,
    view_count,
    forward_count,
    message_date
FROM {{ ref('stg_telegram_messages') }}