{{ config(materialized='view')}}

SELECT 
    order_id,
    payment_sequential as sequential,
    payment_type,
    payment_installments as installments,
    payment_value

FROM {{ source('olist_raw','order_payments')}}