-- View counts should never be negative
SELECT *
FROM "medical_db"."staging_marts"."fct_messages"
WHERE view_count < 0