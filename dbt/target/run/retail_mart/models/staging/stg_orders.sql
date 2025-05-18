
  create view "warehouse"."public"."stg_orders__dbt_tmp"
    
    
  as (
    SELECT 
    id,
    user_id,
    is_refund,
    created_at,
    updated_at
FROM "warehouse"."public"."orders"
  );