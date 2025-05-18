WITH order_items_with_price AS (
    SELECT 
        oi.id,
        oi.order_id,
        oi.goods_id,
        oi.qty,
        g.price,
        oi.created_at,
        o.user_id
    FROM "warehouse"."public"."stg_order_item" oi
    LEFT JOIN "warehouse"."public"."stg_orders" o ON oi.order_id = o.id
    LEFT JOIN "warehouse"."public"."stg_goods" g ON oi.goods_id = g.id
)

SELECT 
    id as order_item_id,
    order_id,
    goods_id,
    user_id,
    qty as quantity,
    price as unit_price,
    qty * price as total_purchase_value,
    created_at as transaction_timestamp
FROM order_items_with_price