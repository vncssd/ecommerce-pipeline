{{ config(materialized='table') }}

SELECT
    oi.order_id,
    oi.product_id,
    oi.seller_id,
    o.customer_id,
    DATE(o.purchased_at) AS date_id,
    o.status,
    oi.price AS item_price,
    oi.freight_value,
    p.payment_type,
    p.installments,
    p.payment_value AS total_payment,
    r.score AS review_score,
    DATEDIFF('day', o.purchased_at, o.delivered_customer_date) AS delivery_days
FROM {{ ref('stg_order_items') }} oi
JOIN {{ ref('stg_orders') }} o ON o.order_id = oi.order_id
JOIN {{ ref('stg_order_payments') }} p ON p.order_id = oi.order_id
LEFT JOIN {{ ref('stg_order_reviews') }} r ON r.order_id = oi.order_id