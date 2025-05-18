
  create view "warehouse"."public"."stg_users__dbt_tmp"
    
    
  as (
    SELECT 
    id,
    name,
    email,
    phone,
    created_at,
    updated_at
FROM "warehouse"."public"."users"
  );