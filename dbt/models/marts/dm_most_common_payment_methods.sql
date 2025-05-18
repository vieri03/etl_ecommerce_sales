SELECT payment_method, COUNT(*) AS num
FROM {{ ref('stg_customers') }}
GROUP BY payment_method
ORDER BY num DESC