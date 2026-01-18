
  
    

  create  table "medical_db"."staging"."fct_messages__dbt_tmp"
  
  
    as
  
  (
    

SELECT
    message_id,
    MD5(channel_name) AS channel_key,
    message_date,
    message_text,
    views AS view_count,
    forwards AS forward_count
FROM "medical_db"."staging"."stg_telegram_messages"
  );
  