SELECT customer_id, SUM(purchase_amount_usd) AS total_spent
FROM {{ ref('stg_customers') }} 
GROUP BY customer_id
ORDER BY total_spent DESC
LIMIT 50