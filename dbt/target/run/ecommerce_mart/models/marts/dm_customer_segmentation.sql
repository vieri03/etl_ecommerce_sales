
  
    
    
    
        
         


        insert into `warehouse`.`dm_customer_segmentation__dbt_backup`
        ("age", "gender", "total")SELECT age, gender, COUNT(*) AS total 
FROM `warehouse`.`stg_customers` 
GROUP BY age, gender ORDER BY total DESC
  