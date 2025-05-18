SELECT age, gender, COUNT(*) AS total 
FROM {{ ref('stg_customers') }} 
GROUP BY age, gender ORDER BY total DESC