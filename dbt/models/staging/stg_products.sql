with source as (
    select * from {{ source('thelook', 'products') }}
)

select
    cast(id as int64) as product_id,
    trim(name) as product_name,
    trim(category) as product_category,
    trim(brand) as brand,
    trim(department) as department,
    cast(cost as numeric) as unit_cost,
    cast(retail_price as numeric) as retail_price,
    cast(distribution_center_id as int64) as distribution_center_id
from source
where id is not null
