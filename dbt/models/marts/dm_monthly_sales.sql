SELECT toStartOfMonth(time_stamp) AS month, COUNT(*) AS sales_count
FROM {{ ref('stg_sales') }}
GROUP BY month
ORDER BY month