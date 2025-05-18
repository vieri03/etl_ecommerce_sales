SELECT user_id, product_id, interaction_type, time_stamp
FROM {{ source('raw', 'sales') }}