
  
    
    
    
        
         


        insert into `warehouse`.`dm_customers_with_highest_purchase_amount__dbt_backup`
        ("customer_id", "total_spent")SELECT customer_id, SUM(purchase_amount_usd) AS total_spent
FROM `warehouse`.`stg_customers` 
GROUP BY customer_id
ORDER BY total_spent DESC
LIMIT 50
  