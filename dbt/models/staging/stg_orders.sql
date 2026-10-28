with source as (
    select * from {{ source('thelook', 'orders') }}
)

select
    cast(order_id as int64) as order_id,
    cast(user_id as int64) as user_id,
    lower(trim(status)) as order_status,
    timestamp(created_at) as created_at,
    timestamp(shipped_at) as shipped_at,
    timestamp(delivered_at) as delivered_at,
    timestamp(returned_at) as returned_at,
    cast(num_of_item as int64) as num_items
from source
where order_id is not null
