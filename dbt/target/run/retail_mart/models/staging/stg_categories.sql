
  create view "warehouse"."public"."stg_categories__dbt_tmp"
    
    
  as (
    SELECT 
    id,
    name,
    created_at,
    updated_at
FROM "warehouse"."public"."categories"
  );