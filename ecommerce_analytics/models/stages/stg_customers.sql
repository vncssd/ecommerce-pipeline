{{ config(materialized='view')}}

SELECT
    customer_id,
    customer_unique_id as customer_person_id,
    customer_zip_code_prefix as zip_code_prefix,
    customer_city as city,
    customer_state as state

FROM {{ source('olist_raw', 'customers')}}