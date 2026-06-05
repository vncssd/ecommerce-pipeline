{{ config(materialized='table') }}

SELECT DISTINCT
    toDate(parseDateTimeBestEffort(purchased_at)) AS date_id,
    toYear(parseDateTimeBestEffort(purchased_at)) AS year,
    toMonth(parseDateTimeBestEffort(purchased_at)) AS month,
    toDayOfMonth(parseDateTimeBestEffort(purchased_at)) AS day,
    toDayOfWeek(parseDateTimeBestEffort(purchased_at)) AS day_of_week,
    toQuarter(parseDateTimeBestEffort(purchased_at)) AS quarter
FROM {{ ref('stg_orders') }}
WHERE purchased_at IS NOT NULL