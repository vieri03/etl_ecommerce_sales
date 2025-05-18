
  create view "warehouse"."public"."stg_order_items__dbt_tmp"
    
    
  as (
    SELECT 
    id,
    order_id,
    goods_id,
    qty,
    created_at,
    updated_at
FROM "warehouse"."public"."order_items"
  );