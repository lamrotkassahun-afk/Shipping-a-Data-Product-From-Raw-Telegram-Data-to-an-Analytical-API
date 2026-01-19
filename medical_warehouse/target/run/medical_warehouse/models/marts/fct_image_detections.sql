
  
    

  create  table "medical_db"."staging_marts"."fct_image_detections__dbt_tmp"
  
  
    as
  
  (
    

WITH yolo_data AS (
    SELECT
        message_id,
        image_category,
        confidence_score
    FROM "medical_db"."staging"."yolo_detections"
),

message_data AS (
    SELECT
        message_id,
        channel_name,
        view_count
    FROM "medical_db"."staging_staging"."stg_telegram_messages" -- Reference staging here
)

SELECT
    m.message_id,
    m.channel_name,
    y.image_category,
    y.confidence_score,
    m.view_count
FROM yolo_data y
JOIN message_data m ON y.message_id = m.message_id
  );
  