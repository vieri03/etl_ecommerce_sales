
  create view "warehouse"."public"."stg_goods__dbt_tmp"
    
    
  as (
    SELECT 
    id,
    category_id,
    name,
    price,
    created_at,
    updated_at
FROM "warehouse"."public"."goods"
  );