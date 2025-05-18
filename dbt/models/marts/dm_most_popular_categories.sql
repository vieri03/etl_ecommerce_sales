SELECT category, COUNT(*) AS product_count
FROM {{ ref('stg_products') }}
GROUP BY category
ORDER BY product_count DESC