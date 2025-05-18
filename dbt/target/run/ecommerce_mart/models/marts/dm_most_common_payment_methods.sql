
  
    
    
    
        
         


        insert into `warehouse`.`dm_most_common_payment_methods__dbt_backup`
        ("payment_method", "num")SELECT payment_method, COUNT(*) AS num
FROM `warehouse`.`stg_customers`
GROUP BY payment_method
ORDER BY num DESC
  