# 📊 Müşteri Segmentasyonu API

Bu proje, bir e-ticaret veritabanı üzerinden **müşteri**, **ürün**, **tedarikçi** ve **ülke bazlı segmentasyon** işlemleri gerçekleştirerek, kullanıcıların daha anlamlı analizler yapabilmesini amaçlar. Segmentasyon işlemleri **DBSCAN algoritması** kullanılarak yapılır ve **FastAPI** framework'ü ile RESTful servisler sunulur.

---

## 🚀 Projenin Amacı

- Müşteri davranışlarını analiz etmek
- Ürünleri satış verilerine göre kümelere ayırmak
- Tedarikçileri performanslarına göre segmente etmek
- Ülkeleri alışveriş profillerine göre gruplamak
- Niş davranış ve anomali gösteren kayıtları (-1 cluster) tespit etmek

---

## 🧪 Segmentasyon Problemleri ve Özellikleri

### 🟥 Problem 1: Müşteri Segmentasyonu
**Amaç:** Müşterilerin alışveriş davranışlarına göre gruplanması ve aykırı verilerin keşfi

**Tablolar:** `customers`, `orders`, `order_details`

**Soru:**  
“Müşterileri sipariş sayısı, toplam harcama ve ortalama sipariş değeri gibi ölçütlere göre gruplayın. Aykırı alışveriş davranışlarına sahip müşterileri tespit edin.”

**Özellik vektörleri:**
- Sipariş sayısı (`total_orders`)
- Toplam harcama (`total_spent`)
- Ortalama sipariş tutarı (`avg_order_value`)

**Yöntem:**  
1. SQL sorgusu ile veriler alınır.  
2. StandardScaler ile normalize edilir.  
3. DBSCAN algoritmasında optimal `eps`, KneeLocator ile belirlenir.  
4. `min_samples=3` ile clustering yapılır.  
5. `cluster = -1` olanlar aykırı (outlier) müşteri olarak sınıflandırılır.  

**Örnek görselleştirme:**  
Müşteriler toplam sipariş ve harcama üzerinden görselleştirilir, her küme farklı renk ile gösterilir.

### 🟦 Problem 2: Ürün Kümeleme (Benzer Ürünler)
**Tablolar:** `Products`, `OrderDetails`

**Soru:**  
“Benzer sipariş geçmişine sahip ürünleri DBSCAN ile gruplandırın. Az satılan ya da alışılmadık kombinasyonlarda geçen ürünleri belirleyin.”

**Özellik vektörleri:**
- Ortalama satış fiyatı
- Satış sıklığı
- Sipariş başına ortalama miktar
- Kaç farklı müşteriye satıldı

**Amaç:**  
Benzer ürünlerin segmentasyonu  
**Cluster = -1** → Belki özel ürünler veya niş ihtiyaçlar

---

### 🟩 Problem 3: Tedarikçi Segmentasyonu
**Tablolar:** `Suppliers`, `Products`, `OrderDetails`

**Soru:**  
“Tedarikçileri sağladıkları ürünlerin satış performansına göre gruplandırın. Az katkı sağlayan veya sıra dışı tedarikçileri bulun.”

**Özellik vektörleri:**
- Tedarik ettiği ürün sayısı
- Bu ürünlerin toplam satış miktarı
- Ortalama satış fiyatı
- Ortalama müşteri sayısı

---

### 🟨 Problem 4: Ülkelere Göre Satış Deseni Analizi
**Tablolar:** `Customers`, `Orders`, `OrderDetails`

**Soru:**  
“Farklı ülkelerden gelen siparişleri DBSCAN ile kümeleyin. Sıra dışı sipariş alışkanlığı olan ülkeleri tespit edin.”

**Özellik vektörleri:**
- Toplam sipariş
- Ortalama sipariş tutarı
- Sipariş başına ürün sayısı

---


---

## 🗂️ Dosya Yapısı

```
DBSCAN/
├── clustering.py             → Ürün segmentasyonu (get_product_clusters)
├── country_segmentation.py  → Ülke segmentasyonu (cluster_countries)
├── segmentation.py          → Müşteri segmentasyonu (get_segmented_data)
├── supplier_clustering.py   → Tedarikçi segmentasyonu (cluster_suppliers)
├── main.py                  → FastAPI endpoint'lerinin tanımlandığı ana dosya
├── config.py                → Veritabanı bağlantı ayarları
```

---

## 🧠 Kullanılan Teknolojiler

- Python + FastAPI
- SQLAlchemy (veritabanı bağlantısı)
- Pandas + Scikit-Learn (veri işleme ve DBSCAN algoritması)
- KneeLocator (DBSCAN için eps parametresi belirleme)

---

## 🧬 AR-GE: `min_samples` ve `eps` Optimizasyonu

- Her segmentasyonda **komşuluk mesafesi grafiği** çıkarılarak `KneeLocator` ile **optimal eps** değeri tespit edilir.
- `min_samples = 3` değeri başlangıç olarak kullanılır. Gelecekte farklı veri boyutları ve kümelenme yapıları için `min_samples` otomatik veya dinamik optimize edilebilir (örn. Elbow yöntemi + Silhouette Score kombinasyonu ile).

---

## 🔗 API Endpoint'leri

| Endpoint | Açıklama |
|----------|----------|
| `GET /segments` | Tüm müşterileri segmentlere ayırır |
| `GET /outliers` | Müşteri segmentasyonundaki aykırı kullanıcıları getirir (`cluster = -1`) |
| `GET /product-clusters` | Ürünleri sipariş geçmişine göre kümeler |
| `GET /niche-products` | Az satılan veya farklılaşmış ürünleri listeler (`cluster = -1`) |
| `GET /supplier-clusters` | Tedarikçileri ürün miktar ve müşteri tabanına göre gruplar |
| `GET /country-clusters` | Ülkeleri alışveriş yoğunluk ve değerlerine göre gruplar |

---

## 🧪 Segmentasyon Özellikleri

- **Müşteri:** Sipariş sayısı, toplam harcama, ortalama sepet tutarı
- **Ürün:** Ortalama fiyat, sipariş sayısı, ortalama miktar, farklı müşteri sayısı
- **Tedarikçi:** Ürün sayısı, toplam satış miktarı, ortalama fiyat, ortalama müşteri sayısı
- **Ülke:** Toplam sipariş, ortalama sipariş değeri, ortalama ürün adedi

---

## 📍 Notlar

- Her segmentasyonda `-1` cluster'ı **aykırı değerleri** temsil eder.
- Veritabanı bağlantı ayarları `config.py` içinde `Config.DATABASE_URL` üzerinden yönetilir.

---

## ⚙️ Kurulum ve Kullanım

```bash
# API'yi çalıştırın
uvicorn DBSCAN.main:app --reload
