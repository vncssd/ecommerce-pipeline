{{ config(materialized='table') }}

SELECT
    product_id,
    category,
    name_length,
    description_length,
    photos_quantity,
    weight_g,
    length_cm,
    height_cm,
    width_cm,
    ROUND((length_cm * height_cm * width_cm) / 1000, 2) AS volume_liters
FROM {{ ref('stg_products') }}