/* En Çok Satış Yapan Çalışanı Bulun - Her çalışanın (Employees) sattığı toplam ürün adedini hesaplayarak,en çok satış yapan 
ilk 3 çalışanı listeleyen bir sorgu yazınız. İpucu: Orders, OrderDetails ve Employees tablolarını kullanarak GROUP BY 
ve ORDER BY yapısını oluşturun. TOP 3 veya LIMIT ile ilk 3 çalışanı seçin.*/

SELECT  O.EMPLOYEE_ID,E.FIRST_NAME || ' '|| E.LAST_NAME AS FULL_NAME, SUM(OD.QUANTITY) AS TOTAL FROM ORDERS O
	JOIN EMPLOYEES E ON O.EMPLOYEE_ID = E.EMPLOYEE_ID
	JOIN ORDER_DETAILS OD ON O.ORDER_ID = OD.ORDER_ID
	GROUP BY O.EMPLOYEE_ID, FULL_NAME
	ORDER BY TOTAL DESC
	LIMIT 3

------------------------------------------------------------------
-- Aynı isim soyisime sahip çalışan olursa hatalı olur.
SELECT E.FIRST_NAME ||' '|| E.LAST_NAME AS EMPLOYEE_NAME, SUM(OD.QUANTITY) AS TOTALSOLD
		FROM EMPLOYEES E
		JOIN ORDERS O ON E.EMPLOYEE_ID = O.EMPLOYEE_ID
		JOIN ORDER_DETAILS OD ON O.ORDER_ID =OD.ORDER_ID
		GROUP BY EMPLOYEE_NAME
		ORDER BY TOTALSOLD DESC
		LIMIT 3;
------------------------------------------------------------------

/* Aylık Satış Trendlerini Bulun - Siparişlerin (Orders) hangi yıl ve ayda ne kadar toplam satış geliri oluşturduğunu hesaplayan ve yıllara
göre sıralayan bir sorgu yazınız. İpucu: Orders ve OrderDetails tablolarını kullanın. Tarih bilgisini yıl ve aya göre gruplayın, 
toplam satış gelirini hesaplayarak sıralayın.*/


SELECT DATE_PART('YEAR', O.ORDER_DATE) AS Y,
			DATE_PART('MONTH',O.ORDER_DATE) AS M,
			SUM(OD.UNIT_PRICE*OD.QUANTITY) AS TOTAL_ORDER FROM ORDERS O 
			JOIN ORDER_DETAILS OD 
			ON O.ORDER_ID = OD.ORDER_ID
			GROUP BY Y,M
			ORDER BY TOTAL_ORDER DESC
			-- ORDER BY Y DESC, M DESC;

-------II. YOL --------------------------------------------------------------------------
SELECT EXTRACT(YEAR FROM O.ORDER_DATE) AS year,
       	EXTRACT(MONTH FROM O.ORDER_DATE) AS month,
	   	SUM(OD.QUANTITY* OD.UNIT_PRICE) AS TOTAL
		FROM ORDERS O
		JOIN ORDER_DETAILS OD ON O.ORDER_ID = OD.ORDER_ID
		GROUP BY YEAR,MONTH
		ORDER BY TOTAL;

			
/* En Karlı Ürün Kategorisini Bulun -  Her ürün kategorisinin (Categories), o kategoriye ait ürünlerden (Products) yapılan satışlar 
sonucunda elde ettiği toplam geliri hesaplayan bir sorgu yazınız. İpucu: Categories, Products, OrderDetails ve Orders tablolarını 
birleştirin. Kategori bazında gelir hesaplaması yaparak en yüksekten en düşüğe sıralayın.*/

SELECT C.CATEGORY_ID,C.CATEGORY_NAME, SUM(OD.QUANTITY * OD.UNIT_PRICE) AS TOTAL_PRICE FROM CATEGORIES C 
			JOIN PRODUCTS P ON C.CATEGORY_ID = P.CATEGORY_ID
			JOIN ORDER_DETAILS OD ON P.PRODUCT_ID = OD.PRODUCT_ID
			GROUP BY C.CATEGORY_ID,C.CATEGORY_NAME
			ORDER BY TOTAL_PRICE DESC
			LIMIT 1 
			
-- Burda P.CATEGORY_ID group by ifadesinde bulunmasa bile sorgu çalıştı. Çünkü PK  den yakalıyor aradaki ilişkiyi yakalıyor.
-- P.PRODUCT_ID birincil anahtar olduğu için, her ürün zaten tek bir kategoriye ait olabilir.
-- PRIMARY KEY olan bir sütunun bağlı olduğu diğer sütunlar, tekil olduğu garanti ediliyorsa PostgreSQL bazen GROUP BY’a eklenmelerini zorunlu tutmaz.
--Örnek
SELECT P.PRODUCT_ID,P.CATEGORY_ID, SUM(OD.QUANTITY * OD.UNIT_PRICE) AS TOTAL_PRICE FROM CATEGORIES C 
			JOIN PRODUCTS P ON C.CATEGORY_ID = P.CATEGORY_ID
			JOIN ORDER_DETAILS OD ON P.PRODUCT_ID = OD.PRODUCT_ID
			GROUP BY P.PRODUCT_ID
			ORDER BY TOTAL_PRICE
----II. YOL ----------------------------------------------------------------------
-- Bu yöntem aynı isimde categori adı olursa ikisini bir categori gibi kabul edecektir.
SELECT C.CATEGORY_NAME, SUM(OD.QUANTITY* OD.UNIT_PRICE) AS TOTAL FROM CATEGORIES C
			JOIN PRODUCTS p ON C.CATEGORY_ID = P.CATEGORY_ID
			JOIN ORDER_DETAILS OD ON P.PRODUCT_ID = OD.PRODUCT_ID
			GROUP BY C.CATEGORY_NAME
			ORDER BY TOTAL DESC
			LIMIT 1
	
/* Belli Bir Tarih Aralığında En Çok Sipariş Veren Müşterileri Bulun -  1997 yılında en fazla sipariş veren ilk 5 müşteriyi listeleyen 
bir sorgu yazınız. İpucu: Orders ve Customers tablolarını birleştirin. WHERE ile 1997 yılını filtreleyin, müşteri bazında sipariş 
sayılarını hesaplayarak sıralayın ve en fazla sipariş veren 5 müşteriyi seçin.*/

SELECT C.CUSTOMER_ID,C.CONTACT_NAME,C.COMPANY_NAME, COUNT(C.CUSTOMER_ID) AS ORDER_COUNT
		FROM CUSTOMERS C 
		JOIN ORDERS O ON C.CUSTOMER_ID = O.CUSTOMER_ID
		WHERE DATE_PART('YEAR',O.ORDER_DATE) = 1997
		GROUP BY C.CUSTOMER_ID
		ORDER BY ORDER_COUNT DESC
		LIMIT 5


---- AYNI SEVİYEDE SİPARİŞ SAYISINA SAHİP MÜŞTERİLER OLABİLİR --------------------------------------------------------------------------

--RANK --> TOTALE GÖRE BAKTIĞINDA AYNI VERİLERİ YİNE SIRALADIĞI İÇİN ATLAYARAK İLERLİYOR.
--DENSE_RANK --> AYNI TOTAL_ORDERSLARI AYNI SIRALAMADA TUTTUĞU İÇİN SAYI ATLAMIYOR.

SELECT * FROM ( 
	SELECT C.COMPANY_NAME, 
		    	DENSE_RANK() OVER (ORDER BY COUNT(O.ORDER_ID) DESC) AS TOTAL, -- aynı değere sahip satırlar aynı sırayı paylaşır ve bir sonraki sıra numarası atlanmaz.
		    	COUNT(O.ORDER_ID) AS TOTAL_ORDERS
			FROM CUSTOMERS C
			JOIN ORDERS O ON C.CUSTOMER_ID = O.CUSTOMER_ID
			WHERE EXTRACT(YEAR FROM O.ORDER_DATE) = 1997
			GROUP BY C.COMPANY_NAME
			ORDER BY TOTAL) CUSTOMER_ORDER_COUNTS
			WHERE TOTAL <= 5

--------------------------- WITH (CTE) KULLANARAK ÇÖZÜM VIA CHATGPT ----------------------------

WITH RankedOrders AS (
    SELECT 
        C.COMPANY_NAME, 
        DENSE_RANK() OVER (ORDER BY COUNT(O.ORDER_ID) DESC) AS RANK,
        COUNT(O.ORDER_ID) AS TOTAL_ORDERS
    FROM CUSTOMERS C
    JOIN ORDERS O ON C.CUSTOMER_ID = O.CUSTOMER_ID
    WHERE EXTRACT(YEAR FROM O.ORDER_DATE) = 1997
    GROUP BY C.COMPANY_NAME
)
SELECT * FROM RankedOrders WHERE RANK <= 5 ORDER BY RANK;

/* Ülkelere Göre Toplam Sipariş ve Ortalama Sipariş Tutarını Bulun - Müşterilerin bulunduğu ülkeye göre toplam sipariş sayısını ve 
ortalama sipariş tutarını hesaplayan bir sorgu yazınız. Sonucu toplam sipariş sayısına göre büyükten küçüğe sıralayın. İpucu: Customers,
Orders ve OrderDetails tablolarını birleştirin. Ülke bazında GROUP BY kullanarak toplam sipariş sayısını ve ortalama sipariş tutarını
hesaplayın.*/

-- BENZERSİZ SİPARİŞ DEĞERİNİ BULALIM --
SELECT DISTINCT ORDER_ID FROM ORDER_DETAILS  -- 830 TANE SİPARİŞ ALINMIŞ
SELECT COUNT(*) FROM ORDER_DETAILS  -- 2155 TANE SİPARİŞ DETAYI KAYDI VAR 
-- BU DURUMDA TOPLAM SİPARİŞ SAYISINI DİKKATE ALMAK İÇİN DISTINCT KULLANMALIYIZ

SELECT 
      C.COUNTRY, 
      COUNT(DISTINCT O.ORDER_ID) AS TOTAL_ORDER_COUNT, 
      AVG(OD.UNIT_PRICE * OD.QUANTITY * (1 - OD.DISCOUNT)) AS AVARAGE_ORDER_AMAOUNT
	FROM CUSTOMERS C
	JOIN ORDERS O ON C.CUSTOMER_ID = O.CUSTOMER_ID
	JOIN ORDER_DETAILS OD ON O.ORDER_ID = OD.ORDER_ID
	GROUP BY C.COUNTRY
	ORDER BY TOTAL_ORDER_COUNT DESC;

---------- İNDİRİM DİKKATE ALINMAZ İSE ----------------------

SELECT C.COUNTRY, COUNT(DISTINCT OD.ORDER_ID) AS TOTAL_ORDERS, AVG(OD.UNIT_PRICE* OD.QUANTITY)
		FROM CUSTOMERS C
		JOIN ORDERS O ON C.CUSTOMER_ID = O.CUSTOMER_ID
		JOIN ORDER_DETAILS OD ON O.ORDER_ID = OD.ORDER_ID
		GROUP BY C.COUNTRY
		ORDER BY TOTAL_ORDERS DESC;

SELECT * FROM ORDER_DETAILS