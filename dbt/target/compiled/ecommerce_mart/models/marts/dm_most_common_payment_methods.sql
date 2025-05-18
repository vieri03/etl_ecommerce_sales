SELECT payment_method, COUNT(*) AS num
FROM `warehouse`.`stg_customers`
GROUP BY payment_method
ORDER BY num DESC