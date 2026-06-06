{{ config(materialized='view')}}

SELECT 
        order_id,
        customer_id,
        order_status as status, 
        TRY_TO_TIMESTAMP(order_purchase_timestamp) as purchased_at,
        TRY_TO_TIMESTAMP(order_approved_at) as approved_at,
        TRY_TO_TIMESTAMP(order_delivered_carrier_date) as delivered_carrier_date,
        TRY_TO_TIMESTAMP(order_delivered_customer_date) as delivered_customer_date,
        TRY_TO_TIMESTAMP(order_estimated_delivery_date) as estimated_delivery

FROM {{ source('olist_raw','orders')}}
