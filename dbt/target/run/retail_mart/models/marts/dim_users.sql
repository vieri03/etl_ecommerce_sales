
  
    

  create  table "warehouse"."public"."dim_users__dbt_tmp"
  
  
    as
  
  (
    WITH latest_transaction AS (
    SELECT 
        user_id,
        MAX(created_at) as last_transaction_timestamp
    FROM "warehouse"."public"."stg_orders" o
    GROUP BY user_id
)
SELECT 
    u.id as user_id,
    u.name,
    u.email,
    u.phone,
    u.created_at as user_created_at,
    lt.last_transaction_timestamp
FROM "warehouse"."public"."stg_users" u
LEFT JOIN latest_transaction lt ON u.id = lt.user_id
  );
  