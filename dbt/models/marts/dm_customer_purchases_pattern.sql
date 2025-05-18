SELECT
  c.gender,
  p.category_level_1,
  COUNT(*) AS purchases
FROM {{ ref('stg_sales') }} s
JOIN {{ ref('stg_customers') }} c ON s.user_id = c.customer_id
JOIN {{ ref('stg_products') }} p ON s.product_id = p.unique_id
GROUP BY c.gender, p.category_level_1
ORDER BY purchases DESC