SELECT age, gender, COUNT(*) AS total 
FROM `warehouse`.`stg_customers` 
GROUP BY age, gender ORDER BY total DESC