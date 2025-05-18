

  create or replace view `warehouse`.`stg_sales` 
  
    
    
  as (
    SELECT user_id, product_id, interaction_type, time_stamp
FROM `warehouse`.`sales`
    
  )
      
      
                    -- end_of_sql
                    
                    