-- SQL HomeWork

-- INNER JOIN SORULARI 

/*Müşterilerin Siparişleri -  Müşteriler (Customers) ve siparişler (Orders) tablolarını kullanarak, 
en az 5 sipariş vermiş müşterilerin adlarını ve verdikleri toplam sipariş sayısını listeleyin.*/

SELECT cus.company_name, cus.contact_name, COUNT(ord.order_id) AS total_order FROM Customers AS cus 
		 INNER JOIN Orders AS ord
		 ON cus.customer_id = ord.customer_id
		 GROUP BY cus.company_name ,cus.contact_name
		 HAVING COUNT(ord.order_id) >= 5;

/* En Çok Satış Yapan Çalışanlar -  Çalışanlar (Employees) ve siparişler (Orders) tablolarını kullanarak, 
her çalışanın toplam kaç sipariş aldığını ve en çok sipariş alan 3 çalışanı listeleyin.*/

SELECT emp.employee_id,emp.first_name, count(ord.order_id) AS total_order_count  FROM Employees AS emp
		INNER JOIN Orders AS ord
		ON emp.employee_id = ord.employee_id
		GROUP BY emp.employee_id,emp.first_name
		ORDER BY total_order_count DESC
		LIMIT 3

/* En Çok Satılan Ürünler -  Sipariş detayları (Order Details) ve ürünler (Products) tablolarını kullanarak, 
toplamda en fazla satılan (miktar olarak) ilk 5 ürünü listeleyin.*/

SELECT ord.product_id,prod.product_name, SUM(ord.quantity) FROM Order_Details AS ord
								  INNER JOIN Products AS prod
								  ON ord.product_id = prod.product_id
								  GROUP BY ord.product_id,prod.product_name 
								  LIMIT 5


/*Her Müşterinin Aldığı Kategoriler -  Müşteriler (Customers), siparişler (Orders), sipariş detayları (Order Details), 
ürünler (Products) ve kategoriler (Categories) tablolarını kullanarak, her müşterinin satın aldığı farklı kategorileri listeleyin.*/

SELECT DISTINCT cus.customer_id, cus.contact_name, cat.category_id, cat.category_name
									FROM Order_Details AS ord_det
									INNER JOIN Orders AS ord ON ord_det.order_id = ord.order_id
									INNER JOIN Customers AS cus ON ord.customer_id = cus.customer_id
									INNER JOIN Products AS prod ON prod.product_id = ord_det.product_id
									INNER JOIN Categories AS cat ON prod.category_id = cat.category_id
									ORDER BY cus.customer_id, cat.category_id

/* Müşteri-Sipariş-Ürün Kombinasyonu -  Müşteriler (Customers), siparişler (Orders), sipariş detayları (Order Details) ve 
ürünler (Products) tablolarını kullanarak, her müşterinin kaç farklı ürün satın aldığını ve toplam kaç adet aldığını listeleyin.*/


SELECT cus.customer_id, cus.contact_name,prod.product_name,
									SUM(ord_det.quantity)
									FROM Order_Details AS ord_det
									INNER JOIN Orders AS ord ON ord_det.order_id = ord.order_id
									INNER JOIN Customers AS cus ON ord.customer_id = cus.customer_id
									INNER JOIN Products AS prod ON prod.product_id = ord_det.product_id
									GROUP BY cus.customer_id,cus.contact_name,prod.product_name
									ORDER BY cus.customer_id -- Bu sorgu müşterinin aldığı her bir ürünü ayrı ayrı gösterir


SELECT cus.customer_id, cus.contact_name,  COUNT(DISTINCT prod.product_id) AS unique_product_count,  -- Satın alınan farklı ürün sayısı
       										SUM(ord_det.quantity) AS total_quantity  -- Toplam alınan ürün adedi
											FROM Order_Details AS ord_det
											INNER JOIN Orders AS ord ON ord_det.order_id = ord.order_id
											INNER JOIN Customers AS cus ON ord.customer_id = cus.customer_id
											INNER JOIN Products AS prod ON prod.product_id = ord_det.product_id
											GROUP BY cus.customer_id, cus.contact_name
											ORDER BY total_quantity DESC  -- En çok ürün alan müşteri en üstte olsun


-- LEFT JOIN SORULARI 
/*Hiç Sipariş Vermeyen Müşteriler - Müşteriler (Customers) ve siparişler (Orders) tablolarını kullanarak, hiç sipariş vermemiş müşterileri listeleyin.*/

SELECT DISTINCT(customer_id) , COUNT(*) 
								FROM Orders 
								GROUP BY customer_id  -- 89 tane farklı müşteri sipariş vermiş 
										 
SELECT COUNT(*) FROM Customers -- 91 tane müşteri var 

SELECT cus.customer_id, cus.contact_name, cus.company_name, ord.order_id
													FROM Customers AS cus 
													LEFT JOIN Orders AS ord
													ON cus.customer_id = ord.customer_id
													WHERE ord.order_id IS NULL -- 2 Tane aipariş vermeyen müşteri var

/*Ürün Satmayan Tedarikçiler -  Tedarikçiler (Suppliers) ve ürünler (Products) tablolarını kullanarak, hiç ürün satmamış tedarikçileri listeleyin.*/

SELECT DISTINCT(supplier_id) , COUNT(*) FROM Products 
										 GROUP BY supplier_id  --29 tane farklı tedarikçi almış ürünleri 

SELECT COUNT(*) FROM Suppliers -- 29 tane tedarikçi var

SELECT sup.supplier_id, sup.contact_name 
								FROM Suppliers AS sup 
								LEFT JOIN Products AS prod
								ON sup.supplier_id = prod.supplier_id
								WHERE prod.product_id IS NULL  -- Hiç ürünü olmayan tedarikçiler

/*Siparişleri Olmayan Çalışanlar -  Çalışanlar (Employees) ve siparişler (Orders) tablolarını kullanarak, hiç sipariş almamış çalışanları listeleyin.*/

SELECT DISTINCT(employee_id) , COUNT(*) 
									FROM Orders 
									GROUP BY employee_id  --9 tane farklı  çalışan sipariş almış 

SELECT COUNT(*) FROM Employees -- 9 tane çalışan var

SELECT emp.employee_id, emp.first_name 
								FROM Orders AS ord 
								LEFT JOIN Employees AS emp
								ON ord.employee_id = emp.employee_id
								WHERE ord.employee_id IS NULL  -- Hiç sipariş almayan çalışanlar
				
SELECT ord.employee_id, emp.first_name 
								FROM Orders AS ord 
								LEFT JOIN Employees AS emp
								ON ord.employee_id = emp.employee_id
								GROUP BY ord.employee_id ,emp.first_name
								HAVING ord.employee_id IS NOT NULL  -- Sipariş alan çalışanlar çalışanlar

-- RIGHT JOIN SORULARI 

/*Her Sipariş İçin Müşteri Bilgisi -  RIGHT JOIN kullanarak, tüm siparişlerin yanında müşteri bilgilerini de listeleyin. 
Eğer müşteri bilgisi eksikse,"Bilinmeyen Müşteri" olarak gösterin.*/

SELECT COUNT(*) FROM  Orders -- 830 tane sipariş var
SELECT COUNT(*) FROM Customers  --  91 tane müşteri
SELECT * FROM Orders Where customer_id IS NULL -- Customer_id' si boş olan kayıt yok - çünkü foreing key kısıtlaması var boş kayıt atmaya engel oluyor.



 --NULL değerlerin yerini belirli bir değerin almasını sağlamak için SQL COALESCE fonksiyonununu kulanalım
SELECT ord.order_id,COALESCE(cus.customer_id, 'Bilinmeyen Müşteri') AS customer_id,
		       				COALESCE(cus.contact_name, 'Bilinmeyen Müşteri') AS contact_name,
			   				COALESCE(cus.region, 'Bilinmeyen Bölge') AS region -- Örnek de görmek için yaptım bunu 
			   				FROM Customers AS cus
			   				RIGHT JOIN Orders AS ord
			   				ON cus.customer_id = ord.customer_id



/* Ürünler ve Kategorileri -  RIGHT JOIN kullanarak, tüm kategoriler ve bu kategorilere ait ürünleri listeleyin. 
Eğer bir kategoriye ait ürün yoksa,kategori adını ve "Ürün Yok" bilgisini gösterin.*/

SELECT COUNT(*) FROM  Categories -- 8 tane kategori var
SELECT COUNT(*) FROM Products  --  77 tane ürün var
SELECT * FROM Products WHERE category_id IS NULL -- category_id' si boş olan kayıt yok - çünkü foreing key kısıtlaması var boş kayıt atmaya engel oluyor.

SELECT cat.category_name, 
       COALESCE(prod.product_name, 'Ürün Yok') AS product_name
	   FROM  Products AS prod
       RIGHT JOIN  Categories AS cat 
       ON prod.category_id = cat.category_id;