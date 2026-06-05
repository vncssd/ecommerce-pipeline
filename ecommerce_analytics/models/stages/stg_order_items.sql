{{ config(materialized='view')}}

SELECT 
    order_id,
    order_item_id as item_id,
    product_id,
    seller_id as seller_id,
    shipping_limit_date,
    price,
    freight_value

FROM {{source('olist_raw', 'order_items')}}