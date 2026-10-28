select
    product_id,
    product_name,
    product_category,
    brand,
    department,
    unit_cost,
    retail_price,
    distribution_center_id
from {{ ref('stg_products') }}
