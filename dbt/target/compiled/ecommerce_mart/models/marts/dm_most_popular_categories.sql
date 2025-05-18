SELECT category, COUNT(*) AS product_count
FROM `warehouse`.`stg_products`
GROUP BY category
ORDER BY product_count DESC