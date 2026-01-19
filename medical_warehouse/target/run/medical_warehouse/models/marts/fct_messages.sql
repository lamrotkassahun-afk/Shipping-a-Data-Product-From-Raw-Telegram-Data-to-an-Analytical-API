
  
    

  create  table "medical_db"."staging_marts"."fct_messages__dbt_tmp"
  
  
    as
  
  (
    

SELECT
    message_id,
    channel_name,
    view_count,
    forward_count,
    message_date
FROM "medical_db"."staging_staging"."stg_telegram_messages"
  );
  