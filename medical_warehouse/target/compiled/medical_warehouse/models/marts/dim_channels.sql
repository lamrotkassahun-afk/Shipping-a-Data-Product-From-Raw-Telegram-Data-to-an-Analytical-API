

SELECT
    MD5(channel_name) AS channel_key,
    channel_name,
    channel_title,
    COUNT(message_id) AS total_messages
FROM "medical_db"."staging_staging"."stg_telegram_messages"
GROUP BY 1, 2, 3