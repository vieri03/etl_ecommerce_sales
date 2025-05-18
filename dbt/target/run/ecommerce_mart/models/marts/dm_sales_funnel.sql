
  
    
    
    
        
         


        insert into `warehouse`.`dm_sales_funnel`
        ("interaction_type", "count")SELECT interaction_type, COUNT(*) AS count
FROM `warehouse`.`stg_sales`
GROUP BY interaction_type
  