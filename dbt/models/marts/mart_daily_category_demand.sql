with sales as (
    select
        f.order_date,
        p.product_category,
        count(*) as units_sold,
        count(distinct f.order_id) as orders,
        sum(f.sale_price) as gross_revenue,
        avg(f.sale_price) as average_selling_price
    from {{ ref('fct_order_items') }} f
    inner join {{ ref('dim_products') }} p using (product_id)
    where f.order_date < current_date()
    group by 1, 2
)

select
    order_date,
    product_category,
    units_sold,
    orders,
    gross_revenue,
    average_selling_price,
    extract(dayofweek from order_date) as day_of_week,
    extract(month from order_date) as month,
    case when extract(dayofweek from order_date) in (1, 7) then true else false end as is_weekend
from sales
