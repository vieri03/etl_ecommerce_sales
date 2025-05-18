
  
    
    
    
        
         


        insert into `warehouse`.`dm_monthly_sales__dbt_backup`
        ("month", "sales_count")SELECT toStartOfMonth(time_stamp) AS month, COUNT(*) AS sales_count
FROM `warehouse`.`stg_sales`
GROUP BY month
ORDER BY month
  