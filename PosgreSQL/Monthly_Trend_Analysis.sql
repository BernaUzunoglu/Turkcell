----------------------------------------------------------------------------
-- SORU -  4 
----------------------------------------------------------------------------

/* 4️ ) Her Müşterinin Siparişlerinde Kullanılan İndirim Oranının Zaman İçinde Nasıl Değiştiğini Bulun - Müşterilerin siparişlerinde 
uygulanan indirim oranlarının zaman içindeki trendini hesaplayan bir sorgu yazın.

Müşteri bazında hareketli ortalama indirim oranlarını hesaplayın ve sipariş tarihine göre artış/azalış eğilimi belirleyin.*/

-- Aylık Trend Analizi

WITH monthly_discounts AS (
    -- Aylık ortalama indirim oranlarını hesaplamak için müşterileri aylık olarak gruplayıp ort. indirim oranlarını hesaplayalım.
    SELECT
        o.customer_id,
        TO_CHAR(o.order_date, 'YYYY-MM') AS order_month, -- Yıl ve ayı al AS order_month, -- Yıl ve ayı al
        AVG(od.discount) AS avg_discount_rate
    FROM
        orders o
    JOIN
        order_details od ON o.order_id = od.order_id
    GROUP BY
        o.customer_id,
        TO_CHAR(o.order_date, 'YYYY-MM')
),
customer_monthly_trend AS (
    -- Müşteri bazında aylık hareketli ortalama ve trend analizi yapmak için customer_id 
    SELECT
        customer_id,
        order_month,
        avg_discount_rate,
        -- Hareketli ortalama hesapla (örneğin son 3 ay)
        AVG(avg_discount_rate) OVER (
            PARTITION BY customer_id
            ORDER BY order_month
            ROWS BETWEEN 2 PRECEDING AND CURRENT ROW
        ) AS moving_avg_discount_rate,
        -- Bir önceki ayın ortalama indirim oranını bul
        LAG(avg_discount_rate, 1) OVER (
            PARTITION BY customer_id
            ORDER BY order_month
        ) AS previous_avg_discount_rate
    FROM
        monthly_discounts
)
SELECT
    customer_id,
    order_month,
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
    customer_monthly_trend
ORDER BY
    customer_id,
    order_month;