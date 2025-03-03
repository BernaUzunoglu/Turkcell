WITH order_discounts AS (
    -- Sipariş bazında ortalama indirim oranını hesapla
    SELECT
        o.customer_id,
        o.order_id,
        o.order_date,
        AVG(od.discount) AS avg_discount_rate
    FROM
        orders o
    JOIN
        order_details od ON o.order_id = od.order_id
    GROUP BY
        o.customer_id,
        o.order_id,
        o.order_date
),
customer_discount_trend AS (
    -- Müşteri bazında 3 siparişlik hareketli ortalama ve trend analizi yap
    SELECT
        customer_id,
        order_id,
        order_date,
        avg_discount_rate,
        -- 3 siparişlik hareketli ortalama
        AVG(avg_discount_rate) OVER (
            PARTITION BY customer_id
            ORDER BY order_date
            ROWS BETWEEN 2 PRECEDING AND CURRENT ROW
        ) AS moving_avg_discount_rate,
        -- Bir önceki siparişin ortalama indirim oranını bul
        LAG(avg_discount_rate, 1) OVER (
            PARTITION BY customer_id
            ORDER BY order_date
        ) AS previous_avg_discount_rate
    FROM
        order_discounts
)
SELECT
    customer_id,
    order_id,
    order_date,
    avg_discount_rate,
    moving_avg_discount_rate,
    previous_avg_discount_rate,
    -- Trendi belirle (artış, azalış, sabit)
    CASE
        WHEN avg_discount_rate > previous_avg_discount_rate THEN 'Artış'
        WHEN avg_discount_rate < previous_avg_discount_rate THEN 'Azalış'
        ELSE 'Sabit'
    END AS discount_trend
FROM
    customer_discount_trend
ORDER BY
    customer_id,
    order_date;