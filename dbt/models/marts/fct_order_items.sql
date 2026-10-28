with items as (
    select * from {{ ref('stg_order_items') }}
),
orders as (
    select order_id, order_status, num_items from {{ ref('stg_orders') }}
)

select
    i.order_item_id,
    i.order_id,
    i.user_id,
    i.product_id,
    date(i.created_at) as order_date,
    i.item_status,
    o.order_status,
    i.sale_price,
    o.num_items
from items i
left join orders o using (order_id)
where i.item_status not in ('cancelled', 'returned')
