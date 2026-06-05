{{ config(materialized='view')}}

SELECT 
    review_id,
    order_id,
    review_score as score,
    review_comment_title as title,
    review_comment_message as message,
    review_creation_date as created_at,
    review_answer_timestamp as answered_at

FROM {{ source('olist_raw', 'order_reviews')}}