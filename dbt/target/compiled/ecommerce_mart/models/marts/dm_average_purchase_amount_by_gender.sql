SELECT gender, AVG(purchase_amount_usd) AS avg_amount
FROM `warehouse`.`stg_customers`
GROUP BY gender