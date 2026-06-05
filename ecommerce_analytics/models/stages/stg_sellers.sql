{{ config(materialized='view')}}

SELECT 
    seller_id,
    seller_zip_code_prefix as zip_code,
    seller_city as city,
    seller_state as state

FROM {{source('olist_raw', 'sellers')}}