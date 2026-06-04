{{ config(materialized='view')}}

SELECT 
        order_id,
        customer_id,
        order_status as status, 
        order_purchase_timestamp as purchased_at,
        order_approved_at as approved_at,
        order_delivered_carrier_date as delivered_carrier_date,
        order_delivered_customer_date as delivered_customer_date,
        order_estimated_delivery_date as estimated_delivery

FROM {{ source('olist_raw','orders')}}
