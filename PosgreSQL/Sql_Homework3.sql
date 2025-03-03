-- AR_GE -> CTE (Common Table Expressions) ve PIVOT

/* Her Çalışanın En Çok Satış Yaptığı Ürünü Bulun - Her çalışanın (Employees) sattığı ürünler içinde en çok sattığı (toplam adet olarak) 
ürünü bulun ve sonucu çalışana göre sıralayın.*/

WITH TOP_SELLING_PRODUCT AS (
	SELECT 
        E.EMPLOYEE_ID,
		E.FIRST_NAME || ' ' || E.LAST_NAME as FULL_NAME,
        OD.PRODUCT_ID,
		P.PRODUCT_NAME,
        SUM(OD.QUANTITY) AS TOTAL,
        RANK() OVER (PARTITION BY E.EMPLOYEE_ID ORDER BY SUM(OD.QUANTITY) DESC) AS RNK --  her çalışanın verileri kendi grubu içinde değerlendirilir.
		FROM EMPLOYEES E 
		JOIN ORDERS O ON E.EMPLOYEE_ID = O.EMPLOYEE_ID 
		JOIN ORDER_DETAILS OD ON O.ORDER_ID = OD.ORDER_ID
		JOIN PRODUCTS P ON P.PRODUCT_ID = OD.PRODUCT_ID
		GROUP BY E.EMPLOYEE_ID,OD.PRODUCT_ID,P.PRODUCT_NAME
)
SELECT EMPLOYEE_ID,FULL_NAME,PRODUCT_ID,PRODUCT_NAME,TOTAL FROM TOP_SELLING_PRODUCT WHERE RNK = 1 ORDER BY EMPLOYEE_ID

---- CTO KULLANMADAN - TABLOLARIN SAĞLAMASINI YAPMAK İÇİN ----------------------------------------------------------
SELECT E.EMPLOYEE_ID,OD.PRODUCT_ID,SUM(OD.QUANTITY) AS TOTAL FROM EMPLOYEES E 
				JOIN ORDERS O ON E.EMPLOYEE_ID = O.EMPLOYEE_ID
				JOIN ORDER_DETAILS OD ON O.ORDER_ID=OD.ORDER_ID
				GROUP BY E.EMPLOYEE_ID,OD.PRODUCT_ID
				ORDER BY E.EMPLOYEE_ID , TOTAL DESC


SELECT E.EMPLOYEE_ID,O.ORDER_ID,OD.* FROM EMPLOYEES E 
				JOIN ORDERS O ON E.EMPLOYEE_ID = O.EMPLOYEE_ID
				JOIN ORDER_DETAILS OD ON O.ORDER_ID=OD.ORDER_ID
				WHERE E.EMPLOYEE_ID = 1 AND OD.PRODUCT_ID = 31
-------------------------------------------------------------------------				

/* Bir Ülkenin Müşterilerinin Satın Aldığı En Pahalı Ürünü Bulun-  Belli bir ülkenin (örneğin "Germany") müşterilerinin verdiği siparişlerde
satın aldığı en pahalı ürünü (UnitPrice olarak) bulun ve hangi müşterinin aldığını listeleyin.*/

WITH MAX_PRICE AS (
    -- Almanya'daki siparişlerde en yüksek fiyatlı ürünü bul
    SELECT MAX(OD.UNIT_PRICE) AS MAX_UNIT_PRICE
	    FROM ORDERS O
	    JOIN CUSTOMERS C ON O.CUSTOMER_ID = C.CUSTOMER_ID
	    JOIN ORDER_DETAILS OD ON O.ORDER_ID = OD.ORDER_ID
	    WHERE C.COUNTRY = 'Germany'
)

SELECT DISTINCT
    OD.PRODUCT_ID, 
    P.PRODUCT_NAME, 
    C.CUSTOMER_ID, 
    C.CONTACT_NAME, 
    OD.UNIT_PRICE AS MAX_UNIT_PRICE
		FROM ORDERS O
		JOIN CUSTOMERS C ON O.CUSTOMER_ID = C.CUSTOMER_ID
		JOIN ORDER_DETAILS OD ON O.ORDER_ID = OD.ORDER_ID
		JOIN PRODUCTS P ON OD.PRODUCT_ID = P.PRODUCT_ID
		JOIN MAX_PRICE MP ON OD.UNIT_PRICE = MP.MAX_UNIT_PRICE  -- En yüksek fiyatı eşleştiriyoruz
		WHERE C.COUNTRY = 'Germany'
		ORDER BY OD.UNIT_PRICE DESC;

----------------------------------------------------------------

SELECT * FROM ORDER_DETAILS WHERE UNIT_PRICE = 263.5
SELECT * FROM ORDERS O 
			JOIN CUSTOMERS C ON O.CUSTOMER_ID = C.CUSTOMER_ID
			JOIN ORDER_DETAILS OD ON O.ORDER_ID = OD.ORDER_ID
			WHERE C.COUNTRY = 'Germany' 
			ORDER BY OD.UNIT_PRICE DESC


/* Her Kategoride (Categories) En Çok Satış Geliri Elde Eden Ürünü Bulun - Her kategori için toplam satış geliri en yüksek olan 
ürünü bulun ve listeleyin.*/
------------------------------------------------------------------------------------------------------------
WITH HIGHEST_REVENUE_PRODUCT_CAT AS (
	SELECT 
	CAT.CATEGORY_ID,
	P.PRODUCT_ID,
	P.PRODUCT_NAME,
	SUM(OD.UNIT_PRICE * OD.QUANTITY * (1-OD.DISCOUNT)) AS HIGHEST_REVENUE,
	 RANK() OVER (PARTITION BY CAT.CATEGORY_ID ORDER BY SUM(OD.UNIT_PRICE * OD.QUANTITY * (1-OD.DISCOUNT)) DESC) AS RNK
	FROM ORDER_DETAILS OD
		JOIN PRODUCTS P ON OD.PRODUCT_ID = P.PRODUCT_ID
		JOIN CATEGORIES CAT ON CAT.CATEGORY_ID = P.CATEGORY_ID
		GROUP BY CAT.CATEGORY_ID,P.PRODUCT_ID
		ORDER BY CAT.CATEGORY_ID, HIGHEST_REVENUE DESC
)
SELECT CATEGORY_ID,PRODUCT_ID,PRODUCT_NAME,HIGHEST_REVENUE FROM HIGHEST_REVENUE_PRODUCT_CAT WHERE RNK = 1

			
/* Arka Arkaya En Fazla Sipariş Veren Müşteriyi Bulun -  Sipariş tarihleri (OrderDate) baz alınarak arka arkaya en fazla sipariş 
veren müşteriyi bulun. (Örneğin, bir müşteri ardışık günlerde kaç sipariş vermiş?)*/
-----------------------------------------
-- LEAD() fonksiyonu ilişkili satırları baz alarak, bir sonraki satıra dair bilgileri döndürür.
--------------------------------------

WITH ORDERED_CUSTOMERS AS (
    SELECT 
        CUSTOMER_ID,
        ORDER_DATE,
        LEAD(ORDER_DATE) OVER (PARTITION BY CUSTOMER_ID ORDER BY ORDER_DATE) AS NEXT_ORDER_DATE
    FROM ORDERS
)
SELECT 
    CUSTOMER_ID,
    COUNT(*) AS CONSECUTIVE_ORDERS
		FROM ORDERED_CUSTOMERS
		WHERE NEXT_ORDER_DATE - ORDER_DATE = 1
		GROUP BY CUSTOMER_ID
		ORDER BY CONSECUTIVE_ORDERS DESC;


------------------------------------------------------------
SELECT CUSTOMER_ID,ORDER_DATE FROM ORDERS 
			GROUP BY CUSTOMER_ID,ORDER_DATE
			ORDER BY CUSTOMER_ID, ORDER_DATE DESC
		
/* Çalışanların Sipariş Sayısına Göre Kendi Departmanındaki Ortalamanın Üzerinde Olup Olmadığını Belirleyin - Her çalışanın aldığı sipariş 
sayısını hesaplayın ve kendi departmanındaki çalışanların ortalama sipariş sayısıyla karşılaştırın. Ortalama sipariş sayısının üstünde 
veya altında olduğunu belirten bir sütun ekleyin.*/

-- Her çalışanın aldığı sipariş sayısını hesaplayın 
SELECT EMPLOYEE_ID, COUNT(*) AS EMP_ORDER_COUNT FROM ORDERS
							GROUP BY EMPLOYEE_ID

-- kendi departmanındaki çalışanların ortalama sipariş sayısıyla karşılaştırın (title departman olarak kabul edelim)
SELECT O.EMPLOYEE_ID,E.TITLE, COUNT(O.ORDER_ID) AS EMP_DEP_ORDER_COUNT FROM ORDERS O 
								JOIN EMPLOYEES E ON O.EMPLOYEE_ID = E.EMPLOYEE_ID
								GROUP BY O.EMPLOYEE_ID,E.TITLE

-----------------------------------------------------------------------------------------
WITH EMPLOYEE_ORDER_COUNT AS (
    -- Çalışan bazında sipariş sayısını hesapla
    SELECT 
        EMPLOYEE_ID, 
        COUNT(*) AS EMP_ORDER_COUNT 
    FROM ORDERS
    GROUP BY EMPLOYEE_ID
),
DEPARTMENT_ORDER_COUNT AS (
    -- Departman bazında çalışanların toplam sipariş sayısını ve ortalamasını hesapla
    SELECT 
        E.TITLE, 
        O.EMPLOYEE_ID,
        COUNT(O.ORDER_ID) AS EMP_DEP_ORDER_COUNT,
        AVG(COUNT(O.ORDER_ID)) OVER (PARTITION BY E.TITLE) AS AVG_DEP_ORDER_COUNT -- departmandaki tüm çalışanların sipariş ortalamasını hesaplar
    FROM ORDERS O
    JOIN EMPLOYEES E ON O.EMPLOYEE_ID = E.EMPLOYEE_ID
    GROUP BY O.EMPLOYEE_ID, E.TITLE
)
SELECT 
    DOC.EMPLOYEE_ID, 
    DOC.TITLE,
    DOC.EMP_DEP_ORDER_COUNT,
    DOC.AVG_DEP_ORDER_COUNT,
    CASE 
        WHEN DOC.EMP_DEP_ORDER_COUNT > DOC.AVG_DEP_ORDER_COUNT THEN 'ÜSTÜNDE'
        WHEN DOC.EMP_DEP_ORDER_COUNT < DOC.AVG_DEP_ORDER_COUNT THEN 'ALTINDA'
        ELSE 'EŞİT'
    END AS ORDER_COMPARISON
FROM DEPARTMENT_ORDER_COUNT DOC
ORDER BY DOC.AVG_DEP_ORDER_COUNT DESC
