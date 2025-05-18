
  
    
    
    
        
         


        insert into `warehouse`.`dm_average_purchase_amount_by_gender__dbt_backup`
        ("gender", "avg_amount")SELECT gender, AVG(purchase_amount_usd) AS avg_amount
FROM `warehouse`.`stg_customers`
GROUP BY gender
  