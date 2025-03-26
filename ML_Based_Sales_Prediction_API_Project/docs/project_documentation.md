# Satış Tahmini API Projesi (Northwind Verisi ile)

## 1. İş Hedefi ve Genel Tanım
Amaç, Northwind veritabanındaki sipariş verilerini kullanarak bir makine öğrenmesi modeli eğitmek ve bu modeli dış dünyaya bir REST API ile sunmaktır. Bu proje sonunda dış sistemler, geçmiş veriyle eğitilmiş modele API üzerinden ürün bazlı satış tahminleri göndererek tahmin sonucunu alabileceklerdir.

---

## 2. Gereksinimler

### 2.1 Teknik Gereksinimler
- **Programlama Dili:** Python 3.x
- **Veri Tabanı:** PostgreSQL (Northwind)
- **API Framework:** FastAPI
- **Makine Öğrenmesi:** scikit-learn
- **Veri İşleme:** pandas, numpy
- **Veri Erişimi:** SQLAlchemy
- **Dokümantasyon:** Swagger (FastAPI ile otomatik)

### 2.2 Fonksiyonel Gereksinimler
- Northwind veritabanından veri çekilecek.
- Gerekli veri ön işleme adımları yapılacak.
- Ürün bazlı geçmiş satış verilerine göre tahmin modeli oluşturulacak.
- API üzerinden:
  - Veri çekme (ürünler, kategoriler vs.)
  - Yeni tahmin sorgusu gönderme
  - Modelin eğitilmesini tetikleme (opsiyonel) yapılabilecek.

---

## 3. Görev Listesi

### A. Veri Tabanı ve Veri İşleme
- Northwind veritabanının kurulumu ve bağlantı testi
- Aşağıdaki tabloların incelenmesi ve veri modelinin çıkarılması:
  - Orders
  - Order_Details
  - Products
  - Customers
  - Categories (opsiyonel)
- Pandas ile verilerin çekilmesi
- Aylık veya ürün bazlı satış özet verisinin hazırlanması
- Eksik veri kontrolü ve temizliği
- **Özellik Mühendisliği:**
  - Ay bilgisi, ürün fiyatı, müşteri segmentasyonu gibi özellikler üretme

### B. Makine Öğrenmesi Modeli
- **Hedef değişken belirleme:** (örnek: ürün bazlı satış miktarı)
- **Eğitim ve test verisinin hazırlanması** (train_test_split)
- **Model seçimi** (Regresyon veya ilgili makine öğrenmesi modelleri)
- **Modelin eğitilmesi ve test edilmesi**
- **Model başarım metriklerinin raporlanması** (R2, RMSE vb.)
- **Eğitilmiş modelin kaydedilmesi** (.pkl formatında)

### C. API Geliştirme
- **FastAPI ile temel yapı kurulumu**
- **Aşağıdaki API uç noktalarının oluşturulması:**

| Endpoint          | Method | Açıklama                         |
|------------------|--------|---------------------------------|
| /products       | GET    | Ürün listesini döner         |
| /predict        | POST   | Tahmin yapılmasını sağlar  |
| /retrain        | POST   | Modeli yeniden eğitir (opsiyonel) |
| /sales_summary  | GET    | Satış özet verisini döner |

- **/predict Uç Noktası:**
  - Kullanıcıdan ürün, tarih ve müşteri bilgilerini alır.
  - Modeli yükler ve tahmini yapar.
  - Tahmini sonucu JSON formatında döner.
- **Swagger dokümantasyonunun kontrolü**

### D. Test ve Dağıtım
- **API uç noktalarının Postman veya Swagger ile test edilmesi**
- **API’ye örnek talepler gönderilmesi**
- **Hata yönetimi ve validasyon mekanizmalarının eklenmesi**
- **Projenin requirements.txt ile dışa aktarılması**
- *(Opsiyonel)* **Docker ile konteyner haline getirme**

---

## 4. Teslim Edilecekler
- **Python kodları ve Jupyter notebook dosyaları**
- **API kodları (FastAPI)**
- **Eğitilmiş model dosyası (.pkl)**
- **README.md:**
  - Projenin amacı
  - Nasıl çalıştırılacağı
  - Örnek API istekleri
- **Swagger veya Postman ile API dokümantasyonu**

---

📂 ML_Based_Sales_Prediction_API/
├── .env.example            -> Örnek çevre değişkenleri şablonu
├── .gitignore              -> Git için ignore dosyası
├── README.md
├── requirements.txt
├── tests/                  -> Unit ve integration testleri
│   ├── test_api.py
│   └── test_models.py
├── docs/
│   ├── API_DOCS.md
│   ├── DATA_DICTIONARY.md  -> Veri yapısı dokümantasyonu
│   └── ARCHITECTURE.md     -> Sistem mimarisi
├── research/              -> Keşifçi Veri Analizi -  ARGE çalışmaları
│   └── EDA.ipynb
├── src/
│   ├── __init__.py
│   ├── api/
│   │   ├── endpoints.py
│   │   └── schemas.py
│   ├── models/
│   │   ├── train_model.py
│   │   └── predict.py
│   ├── data/
│   │   ├── database.py
│   │   └── preprocessing.py
│   └── config.py           -> Konfigürasyon ayarları
└── models/                 -> Eğitilmiş model dosyaları (.pkl)


---