-- Level 3 - Expert
-- AR_GE -> CTE (Common Table Expressions), Window Functions, Recursive Queries, Pivot, Subqueries ve Advanced Aggregation

----------------------------------------------------------------------------
-- SORU -  1 
----------------------------------------------------------------------------

/* 1 ) Her Müşteri İçin En Son 3 Siparişi ve Toplam Harcamalarını Listeleyin  - Her müşterinin en son 3 siparişini 
(OrderDate’e göre en güncel 3 sipariş) ve bu siparişlerde harcadığı toplam tutarı gösteren bir sorgu yazın.
Sonuç müşteri bazında sıralanmalı ve her müşterinin sadece en son 3 siparişi görünmelidir. */

--Her Müşteri için en son  siparişlerini getirelim
SELECT CUSTOMER_ID, ORDER_DATE,
           ROW_NUMBER() OVER (PARTITION BY CUSTOMER_ID ORDER BY ORDER_DATE DESC) AS RN
    FROM ORDERS

-- En son ki 3 siparişi seçelim - bunun için row number sutunu olan bir CTE tanımlayalım
WITH ORDER_TABLE AS (
SELECT CUSTOMER_ID,ORDER_ID, ORDER_DATE,
           ROW_NUMBER() OVER (PARTITION BY CUSTOMER_ID ORDER BY ORDER_DATE DESC) AS RN
    FROM ORDERS
)
SELECT CUSTOMER_ID,ORDER_ID,RN FROM ORDER_TABLE
		WHERE RN <= 3

-- CEVAP 1 )-- En son 3 siparişin totalini hesaplayalım - subquery yazalım ve order_id leri ordan çekelim

WITH TOTAL_AMOUNT AS (
	SELECT CUSTOMER_ID, ORDER_ID,RN
	    FROM (
	        SELECT CUSTOMER_ID, ORDER_ID,
	               ROW_NUMBER() OVER (PARTITION BY CUSTOMER_ID ORDER BY ORDER_DATE DESC) AS RN
	        FROM ORDERS
	    ) AS Ranked
	    WHERE RN <= 3
)
SELECT T.CUSTOMER_ID,ROUND(SUM(OD.UNIT_PRICE * OD.QUANTITY * (1 - OD.DISCOUNT))::NUMERIC,2) AS TOTAL_SPENT, -- double tiplerde round çalışmıyor cast işlemi yaptık ve numeric tipe çevirdik
		-- En son 3 siparişin ORDER_ID'lerini virgülle ayırarak göster
       (SELECT STRING_AGG(ORDER_ID::TEXT, ', ')  -- STRING_AGG() bir grup veri üzerinde birleştirilmiş (concatenated) bir string döndürmek için kullanılır
	        FROM TOTAL_AMOUNT 
	        WHERE CUSTOMER_ID = T.CUSTOMER_ID AND RN <= 3) AS LAST_3_ORDERS
		FROM TOTAL_AMOUNT T
		JOIN ORDER_DETAILS OD ON T.ORDER_ID = OD.ORDER_ID
		GROUP BY T.CUSTOMER_ID
		ORDER BY T.CUSTOMER_ID;

---- CEVAP 2 ) --------------------------------------------------------------
WITH RECENTORDERS AS( -- Müşterinin geçmiş siparişlerini getirelim
	 SELECT
		 O.CUSTOMER_ID,
		 C.COMPANY_NAME,
		 O.ORDER_DATE,
		 SUM(OD.UNIT_PRICE*OD.QUANTITY*(1-OD.DISCOUNT)) AS SPENT,
		 RANK() OVER (PARTITION BY O.CUSTOMER_ID ORDER BY O.ORDER_DATE DESC) AS RNK
	FROM ORDERS O
	JOIN CUSTOMERS C ON C.CUSTOMER_ID = O.CUSTOMER_ID
	JOIN ORDER_DETAILS OD ON O.ORDER_ID = OD.ORDER_ID
	GROUP BY O.CUSTOMER_ID, C.COMPANY_NAME,O.ORDER_ID,O.ORDER_DATE
)
SELECT CUSTOMER_ID,COMPANY_NAME,SUM(SPENT)
		FROM RECENTORDERS
		WHERE RNK <= 3
		GROUP BY CUSTOMER_ID,COMPANY_NAME
		ORDER BY CUSTOMER_ID

--- SAĞLAMASI ----
SELECT ROUND(SUM(UNIT_PRICE * QUANTITY * (1 - DISCOUNT))::NUMERIC,2) AS TOTAL_AMOUNT
	FROM ORDER_DETAILS
	WHERE ORDER_ID IN (11011, 10952, 10835); -- 2250.499996177852 

----------------------------------------------------------------------------
-- SORU -  2 
----------------------------------------------------------------------------

/* 2) Aynı Ürünü 3 veya Daha Fazla Kez Satın Alan Müşterileri Bulun -  Bir müşteri eğer aynı ürünü (ProductID) 3 veya daha fazla sipariş 
verdiyse, bu müşteriyi ve ürünleri listeleyen bir sorgu yazın.
Aynı ürün bir siparişte değil, farklı siparişlerde tekrar tekrar alınmış olabilir. */

-- İlk önce aynı müşterinin birden fazla aldığı ürünleri bulalım.
SELECT O.CUSTOMER_ID, OD.PRODUCT_ID, COUNT(*) AS PRODUCT_COUNT
			FROM ORDERS O
			JOIN ORDER_DETAILS OD ON O.ORDER_ID = OD.ORDER_ID
			GROUP BY O.CUSTOMER_ID, OD.PRODUCT_ID
			ORDER BY O.CUSTOMER_ID, OD.PRODUCT_ID;

-- CEVAP 1 ) - Şimdi en az 3 sipariş koşulunu eklemek için CTE tanımlayıp PRODUCT_COUNT sutununu kullanalım
WITH CUSTOMER_PRODUCT_ORDER_COUNT AS (
	SELECT O.CUSTOMER_ID, OD.PRODUCT_ID, COUNT(*) AS PRODUCT_COUNT
			FROM ORDERS O
			JOIN ORDER_DETAILS OD ON O.ORDER_ID = OD.ORDER_ID
			GROUP BY O.CUSTOMER_ID, OD.PRODUCT_ID
)
SELECT * FROM CUSTOMER_PRODUCT_ORDER_COUNT WHERE PRODUCT_COUNT >2

--SAĞLAMASI-----
SELECT * FROM ORDERS O JOIN ORDER_DETAILS OD
				ON O.ORDER_ID =OD.ORDER_ID
				WHERE O.CUSTOMER_ID = 'LAMAI' AND OD.PRODUCT_ID =  36
				
--- CEVAP 2 ) -----------------------------------------------------------------
SELECT
    C.CUSTOMER_ID,
    C.COMPANY_NAME,
    OD.PRODUCT_ID,
    P.PRODUCT_NAME,
    SUM(OD.QUANTITY) AS TotalQuantity
FROM CUSTOMERS C
JOIN ORDERS O ON C.CUSTOMER_ID = O.CUSTOMER_ID
JOIN ORDER_DETAILS OD ON O.ORDER_ID = OD.ORDER_ID
JOIN PRODUCTS P ON OD.PRODUCT_ID = P.PRODUCT_ID
	GROUP BY C.CUSTOMER_ID, C.COMPANY_NAME, OD.PRODUCT_ID, P.PRODUCT_NAME
	HAVING SUM(OD.QUANTITY) >= 3
	order by totalquantity DESC; -- quantity bazında alırsak
--------------------------------------------------------------------------------
select * from orders o
JOIN ORDER_DETAILS OD ON O.ORDER_ID = OD.ORDER_ID
where customer_id = 'ERNSH' and od.product_id = 24
--------------------------------------------------------------------------------
SELECT
    C.CUSTOMER_ID,
    C.COMPANY_NAME,
    OD.PRODUCT_ID,
    P.PRODUCT_NAME,
    COUNT(O.ORDER_ID) AS OrderCount
FROM CUSTOMERS C
JOIN ORDERS O ON C.CUSTOMER_ID = O.CUSTOMER_ID
JOIN ORDER_DETAILS OD ON O.ORDER_ID = OD.ORDER_ID
JOIN PRODUCTS P ON OD.PRODUCT_ID = P.PRODUCT_ID
GROUP BY
    C.CUSTOMER_ID,
    C.COMPANY_NAME,
    OD.PRODUCT_ID,
    P.PRODUCT_NAME
HAVING COUNT(O.ORDER_ID) >= 3
order by customer_id asc, ordercount desc; --order_id üzerinden hesaplarsak

----------------------------------------------------------------------------
-- SORU -  3 
----------------------------------------------------------------------------

/*3 )  Bir Çalışanın 30 Gün İçinde Verdiği Siparişlerin Bir Önceki 30 Güne Göre Artış/ Azalışını Hesaplayın - Her çalışanın (Employees), 
sipariş sayısının son 30 gün içinde bir önceki 30 güne kıyasla nasıl değiştiğini hesaplayan bir sorgu yazın.
Çalışan bazında sipariş sayısı artış/azalış yüzdesi hesaplanmalı. */

-- İlk önce çalışanların versiği sipariş sayısını bulalım
SELECT EMPLOYEE_ID, COUNT(ORDER_ID) AS ORDER_COUNT FROM ORDERS -- count(*) da görür :)
					GROUP BY EMPLOYEE_ID
					ORDER BY ORDER_COUNT DESC 

-- Şimdi de her çalışanın 30 gün içerisindeki sipariş sayısını bulalım
SELECT ORDER_DATE FROM ORDERS ORDER BY ORDER_DATE DESC LIMIT 1 -- "1998-05-06" En son bu tarihte sipariş alınmış bu tarihi baz alarak işlem yapalım 
SELECT MAX(ORDER_DATE) FROM ORDERS

SELECT EMPLOYEE_ID,COUNT(ORDER_ID) AS ORDER_COUNT  FROM ORDERS 
				WHERE ORDER_DATE >='1998-05-06'::DATE - INTERVAL '30 days'
			GROUP BY EMPLOYEE_ID 

-- Şimdide bir önceki 30 güne ait sipariş sayısını bulalım. 30-60 gün arasını- arasında dediği için between işimizi görür

SELECT EMPLOYEE_ID,COUNT(ORDER_ID) AS ORDER_COUNT 
	FROM ORDERS
	WHERE ORDER_DATE BETWEEN '1998-05-06'::DATE - INTERVAL '60 days'
	                      AND '1998-05-06'::DATE - INTERVAL '30 days'
						  GROUP BY EMPLOYEE_ID ;

---- Dinamik bir şekilde allalım son tarihi
SELECT EMPLOYEE_ID, COUNT(ORDER_ID) AS ORDER_COUNT
FROM ORDERS
WHERE ORDER_DATE BETWEEN 
      (SELECT MAX(ORDER_DATE) FROM ORDERS) - INTERVAL '60 days'
  AND (SELECT MAX(ORDER_DATE) FROM ORDERS) - INTERVAL '30 days'
GROUP BY EMPLOYEE_ID;


-- Çalışan bazında sipariş sayısı artış/azalış yüzdesi hesaplanmalı.
----------------------------------------------------------------
-- Hesaplama : ((Yeni Değer - Eski Değer)/Eski Değer) * 100
----------------------------------------------------------------

WITH LastOrderDate AS (
    SELECT MAX(ORDER_DATE) AS last_order_date FROM ORDERS
),
MONTH_ORDER_COUNT AS (
    SELECT EMPLOYEE_ID, COUNT(ORDER_ID) AS MONTH_ORDER_COUNT
    FROM ORDERS, LastOrderDate  -- LastOrderDate tablosu burda bir nevi altsorgu gibi kullanabiliyoruz. Direk dahil edebiliyoruz
    WHERE ORDER_DATE >= last_order_date - INTERVAL '30 days'
    GROUP BY EMPLOYEE_ID
),
PREV_MONTH_ORDER_COUNT AS (
    SELECT EMPLOYEE_ID, COUNT(ORDER_ID) AS PREV_MONTH_ORDER_COUNT
    FROM ORDERS, LastOrderDate
    WHERE ORDER_DATE BETWEEN last_order_date - INTERVAL '60 days' 
                        AND last_order_date - INTERVAL '30 days'
    GROUP BY EMPLOYEE_ID
)
SELECT 
    MOC.EMPLOYEE_ID,
    MOC.MONTH_ORDER_COUNT,
    PMOC.PREV_MONTH_ORDER_COUNT,
    ROUND(
        ((MOC.MONTH_ORDER_COUNT - PMOC.PREV_MONTH_ORDER_COUNT)::NUMERIC / 
        NULLIF(PMOC.PREV_MONTH_ORDER_COUNT, 0)) * 100, 2  -- 0' a bölme hatasını engellemk için nullif kullandık. eğer değer 0 ise null değerini kullan
    ) AS PERCENT_CHANGE
FROM MONTH_ORDER_COUNT MOC
JOIN PREV_MONTH_ORDER_COUNT PMOC 
ON MOC.EMPLOYEE_ID = PMOC.EMPLOYEE_ID
ORDER BY EMPLOYEE_ID;


----- II . YOL ------------------------------------------------------------------

WITH MONTH_ORDER_COUNT AS (
	SELECT EMPLOYEE_ID,COUNT(ORDER_ID) AS MONTH_ORDER_COUNT  FROM ORDERS 
				WHERE ORDER_DATE >='1998-05-06'::DATE - INTERVAL '30 days'
			GROUP BY EMPLOYEE_ID 

),
PREV_MONTH_ORDER_COUNT AS (
SELECT EMPLOYEE_ID,COUNT(ORDER_ID) AS PREV_MONTH_ORDER_COUNT 
	FROM ORDERS
	WHERE ORDER_DATE BETWEEN '1998-05-06'::DATE - INTERVAL '60 days'
	                      AND '1998-05-06'::DATE - INTERVAL '30 days'
						  GROUP BY EMPLOYEE_ID 
)
SELECT MOC.EMPLOYEE_ID,MOC.MONTH_ORDER_COUNT,PMOC.PREV_MONTH_ORDER_COUNT,
						 ROUND((((MOC.MONTH_ORDER_COUNT - PMOC.PREV_MONTH_ORDER_COUNT)::NUMERIC / PMOC.PREV_MONTH_ORDER_COUNT) * 100),2)  AS PERCENT_CHANGE 
						FROM MONTH_ORDER_COUNT MOC JOIN  PREV_MONTH_ORDER_COUNT PMOC 
						ON MOC.EMPLOYEE_ID = PMOC.EMPLOYEE_ID
						ORDER BY EMPLOYEE_ID

----------------------------------------------------------------------------
-- SORU -  4 
----------------------------------------------------------------------------

/* 4️ ) Her Müşterinin Siparişlerinde Kullanılan İndirim Oranının Zaman İçinde Nasıl Değiştiğini Bulun - Müşterilerin siparişlerinde 
uygulanan indirim oranlarının zaman içindeki trendini hesaplayan bir sorgu yazın.

Müşteri bazında hareketli ortalama indirim oranlarını hesaplayın ve sipariş tarihine göre artış/azalış eğilimi belirleyin.*/

WITH monthly_discounts AS (
    SELECT 
        c.customer_id,
        extract(year from o.order_date) AS order_year,
        extract(month from o.order_date) AS order_month,
        AVG(od.discount) AS avg_discount
    FROM orders o
    JOIN order_details od ON od.order_id = o.order_id
    JOIN customers c ON c.customer_id = o.customer_id
    GROUP BY c.customer_id, order_year, order_month
),
trend_analysis AS (
    SELECT 
        customer_id,
        order_year,
        order_month,
        avg_discount,
        -- Önceki ayın indirim oranı
        LAG(avg_discount) OVER (
            PARTITION BY customer_id 
            ORDER BY order_year, order_month
        ) AS prev_discount,
        -- Son 3 ayın hareketli ortalaması
        AVG(avg_discount) OVER (
            PARTITION BY customer_id 
            ORDER BY order_year, order_month
            ROWS BETWEEN 2 PRECEDING AND CURRENT ROW
        )AS moving_avg_discount
    FROM monthly_discounts
)
SELECT 
    customer_id,
    order_year,
    order_month,
    avg_discount,
    COALESCE(prev_discount, 0) AS prev_discount,
    COALESCE(moving_avg_discount, 0) AS moving_avg_discount,
    -- Geçen aya göre artış/azalış
    CASE
        WHEN avg_discount > COALESCE(prev_discount, 0) THEN 'artış'
        WHEN avg_discount < COALESCE(prev_discount, 0) THEN 'azalış'
        ELSE 'değişim yok'
    END AS trend_monthly,
    -- Hareketli ortalamaya göre trend analizi
    CASE
        WHEN avg_discount > COALESCE(moving_avg_discount, 0) THEN 'artış'
        WHEN avg_discount < COALESCE(moving_avg_discount, 0) THEN 'azalış'
        ELSE 'değişim yok'
    END AS trend_moving_avg
FROM trend_analysis

