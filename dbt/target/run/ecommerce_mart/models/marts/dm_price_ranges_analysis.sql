
  
    
    
    
        
         


        insert into `warehouse`.`dm_price_ranges_analysis__dbt_backup`
        ("price_range", "count")SELECT
  CASE
    WHEN (selling_price_upper) < 20 THEN '<$20'
    WHEN (selling_price_upper) < 50 THEN '$20-49'
    WHEN (selling_price_upper) < 100 THEN '$50-99'
    ELSE '$100+'
  END AS price_range,
  COUNT(*) AS count
FROM `warehouse`.`stg_products`
GROUP BY price_range
  