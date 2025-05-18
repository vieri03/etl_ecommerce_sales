
  
    
    
    
        
         


        insert into `warehouse`.`dm_subscription_effectiveness__dbt_backup`
        ("subscription_status", "avg_spent")SELECT subscription_status, AVG(purchase_amount_usd) AS avg_spent
FROM `warehouse`.`stg_customers`
GROUP BY subscription_status
  