SELECT interaction_type, COUNT(*) AS count
FROM `warehouse`.`stg_sales`
GROUP BY interaction_type