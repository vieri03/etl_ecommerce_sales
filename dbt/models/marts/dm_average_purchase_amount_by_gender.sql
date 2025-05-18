SELECT gender, AVG(purchase_amount_usd) AS avg_amount
FROM {{ ref('stg_customers') }}
GROUP BY gender