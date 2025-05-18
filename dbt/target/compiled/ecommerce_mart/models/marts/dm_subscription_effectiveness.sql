SELECT subscription_status, AVG(purchase_amount_usd) AS avg_spent
FROM `warehouse`.`stg_customers`
GROUP BY subscription_status