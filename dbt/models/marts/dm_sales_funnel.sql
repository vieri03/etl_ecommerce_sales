SELECT interaction_type, COUNT(*) AS count
FROM {{ ref('stg_sales') }}
GROUP BY interaction_type