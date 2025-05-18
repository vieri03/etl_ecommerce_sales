SELECT subscription_status, AVG(purchase_amount_usd) AS avg_spent
FROM {{ ref('stg_customers') }}
GROUP BY subscription_status