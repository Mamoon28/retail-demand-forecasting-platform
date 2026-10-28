with source as (
    select * from {{ source('thelook', 'order_items') }}
)

select
    cast(id as int64) as order_item_id,
    cast(order_id as int64) as order_id,
    cast(user_id as int64) as user_id,
    cast(product_id as int64) as product_id,
    lower(trim(status)) as item_status,
    timestamp(created_at) as created_at,
    timestamp(shipped_at) as shipped_at,
    timestamp(delivered_at) as delivered_at,
    timestamp(returned_at) as returned_at,
    cast(sale_price as numeric) as sale_price
from source
where id is not null
