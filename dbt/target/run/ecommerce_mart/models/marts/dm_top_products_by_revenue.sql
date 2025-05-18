
  
    
    
    
        
         


        insert into `warehouse`.`dm_top_products_by_revenue`
        ("product_name", "sales_count", "avg_price_lower", "est_revenue_lower", "avg_price_upper", "est_revenue_upper")SELECT
  p.product_name,
  COUNT(*) AS sales_count,
  AVG(p.selling_price_lower) AS avg_price_lower,
  COUNT(*) * AVG(p.selling_price_lower) AS est_revenue_lower,
  AVG(p.selling_price_upper) AS avg_price_upper,
  COUNT(*) * AVG(p.selling_price_upper) AS est_revenue_upper
FROM `warehouse`.`sales` s
JOIN `warehouse`.`stg_products` p ON s.product_id = p.unique_id
GROUP BY p.product_name
ORDER BY est_revenue_upper desc
LIMIT 10
  