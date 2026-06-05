{{ config(materialized='table') }}

SELECT
    seller_id,
    zip_code,
    city,
    state,
    CASE
        WHEN state IN ('SP', 'RJ', 'MG', 'ES') THEN 'Sudeste'
        WHEN state IN ('PR', 'SC', 'RS') THEN 'Sul'
        WHEN state IN ('BA', 'PE', 'CE', 'MA', 'PB', 'RN', 'AL', 'SE', 'PI') THEN 'Nordeste'
        WHEN state IN ('AM', 'PA', 'AC', 'RO', 'RR', 'AP', 'TO') THEN 'Norte'
        WHEN state IN ('MT', 'MS', 'GO', 'DF') THEN 'Centro-Oeste'
    END AS region
FROM {{ ref('stg_sellers') }}