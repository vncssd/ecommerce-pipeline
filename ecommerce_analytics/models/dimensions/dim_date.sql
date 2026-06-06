{{ config(materialized='table') }}

SELECT DISTINCT
    DATE(purchased_at) AS date_id,
    YEAR(purchased_at) AS year,
    MONTH(purchased_at) AS month,
    DAY(purchased_at) AS day,
    DAYOFWEEK(purchased_at) AS day_of_week,
    QUARTER(purchased_at) AS quarter
FROM {{ ref('stg_orders') }}
WHERE purchased_at IS NOT NULL