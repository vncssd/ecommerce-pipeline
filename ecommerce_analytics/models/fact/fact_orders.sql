{{ config(materialized='table') }}

SELECT
    oi.order_id,
    oi.product_id,
    oi.seller_id,
    o.customer_id,
    toDate(parseDateTimeBestEffort(o.purchased_at)) AS date_id,
    o.status,
    oi.price AS item_price,
    oi.freight_value AS freight_value,
    p.payment_type,
    p.installments,
    p.payment_value AS total_payment,
    r.score AS review_score,
    dateDiff('day',
        parseDateTimeBestEffortOrNull(o.purchased_at),
        parseDateTimeBestEffortOrNull(nullIf(o.delivered_customer_date, ''))
    ) AS delivery_days
FROM {{ ref('stg_order_items') }} oi
JOIN {{ ref('stg_orders') }} o ON o.order_id = oi.order_id
JOIN {{ ref('stg_order_payments') }} p ON p.order_id = oi.order_id
LEFT JOIN {{ ref('stg_order_reviews') }} r ON r.order_id = oi.order_id