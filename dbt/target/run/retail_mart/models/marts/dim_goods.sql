
  
    

  create  table "warehouse"."public"."dim_goods__dbt_tmp"
  
  
    as
  
  (
    SELECT 
    g.id as goods_id,
    g.name as goods_name,
    g.price as goods_price,
    c.id as category_id,
    c.name as category_name,
    g.created_at as goods_created_at
FROM "warehouse"."public"."stg_goods" g
LEFT JOIN "warehouse"."public"."stg_categories" c ON g.category_id = c.id
  );
  