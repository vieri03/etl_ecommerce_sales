
  
    
    
    
        
         


        insert into `warehouse`.`dm_most_popular_categories__dbt_backup`
        ("category", "product_count")SELECT category, COUNT(*) AS product_count
FROM `warehouse`.`stg_products`
GROUP BY category
ORDER BY product_count DESC
  