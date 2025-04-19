# Film Öneri Sistemi

Bu proje, Netflix benzeri bir film öneri sistemi uygulamasıdır. Kullanıcıların izleme tercihlerine göre film önerileri yapmak için K-means kümeleme algoritması kullanılmaktadır.

## Özellikler

- Kullanıcı yönetimi
- Film ekleme ve kategorilendirme
- Film izleme ve puanlama
- Kişiselleştirilmiş film önerileri
- PostgreSQL veritabanı entegrasyonu
- FastAPI ile RESTful API

## Kurulum

1. Gerekli paketleri yükleyin:
```bash
pip install -r requirements.txt
```

2. PostgreSQL veritabanını oluşturun:
```bash
createdb netflix_recommender
```

3. `.env` dosyası oluşturun ve veritabanı bağlantı bilgilerini ekleyin:
```
DATABASE_URL=postgresql://kullanici:sifre@localhost/netflix_recommender
```

4. Uygulamayı başlatın:
```bash
uvicorn main:app --reload
```

## API Endpoints

- `POST /filmler/` - Yeni film ekle
- `POST /kullanicilar/` - Yeni kullanıcı oluştur
- `POST /puanlar/` - Film puanla
- `POST /izlemeler/` - Film izleme kaydı oluştur
- `GET /oneriler/{kullanici_id}` - Kullanıcıya özel film önerileri al

## Öneri Sistemi

Öneri sistemi şu adımları izler:
1. Filmleri özelliklerine göre kümeler
2. Kullanıcının izleme geçmişini analiz eder
3. Kullanıcının tercih ettiği kümeye göre öneriler yapar
4. Önerilen filmleri IMDB puanına göre sıralar

## Veritabanı Şeması

- `kullanicilar`: Kullanıcı bilgileri
- `filmler`: Film bilgileri
- `kategoriler`: Film kategorileri
- `film_kategori`: Film-kategori ilişkileri
- `izlemeler`: Kullanıcı izleme kayıtları
- `puanlar`: Kullanıcı film puanları 